import streamlit as st
import pandas as pd
import plotly.express as px

# Mengatur judul halaman dan konfigurasi tampilan
st.set_page_config(page_title="Dashboard Analisis E-Commerce", layout="wide")
st.title("Dashboard Analisis Data E-Commerce")

# Fungsi untuk memuat dataset
@st.cache_data
def load_data():
    customers_df = pd.read_csv('E-Commerce Public Dataset/customers_dataset.csv', encoding="latin1")
    orders_df = pd.read_csv('E-Commerce Public Dataset/orders_dataset.csv', encoding="latin1")
    order_items_df = pd.read_csv('E-Commerce Public Dataset/order_items_dataset.csv', encoding="latin1")
    products_df = pd.read_csv('E-Commerce Public Dataset/products_dataset.csv', encoding="latin1")
    order_payments_df = pd.read_csv('E-Commerce Public Dataset/order_payments_dataset.csv', encoding="latin1")
    order_reviews_df = pd.read_csv('E-Commerce Public Dataset/order_reviews_dataset.csv', encoding="latin1")
    
    # Konversi kolom tanggal ke format datetime
    orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
    
    return customers_df, orders_df, order_items_df, products_df, order_payments_df, order_reviews_df

# Memuat data
customers_df, orders_df, order_items_df, products_df, order_payments_df, order_reviews_df = load_data()

# Sidebar Filters
st.sidebar.header('Filter')

# Filter rentang tanggal
min_date = orders_df['order_purchase_timestamp'].min().date()
max_date = orders_df['order_purchase_timestamp'].max().date()
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter berdasarkan provinsi
state_options = ['Semua'] + sorted(customers_df['customer_state'].dropna().unique().tolist())
selected_state = st.sidebar.selectbox('Pilih Provinsi', state_options)

# Filter berdasarkan kategori produk
product_categories = ['Semua'] + sorted(products_df['product_category_name'].dropna().unique().tolist())
selected_category = st.sidebar.selectbox('Pilih Kategori Produk', product_categories)

# Menambahkan informasi di sidebar
st.sidebar.markdown('---')
st.sidebar.markdown(
    "<div style='text-align: center; font-size: 14px;'>"
    "📌 Dashboard ini dibuat untuk analisis data e-commerce. "
    "<br><b>Copyright © 2024 Wisnu Al Hussaeni</b>"
    "</div>",
    unsafe_allow_html=True
)

# Menerapkan filter pada data pesanan
filtered_orders = orders_df[
    (orders_df['order_purchase_timestamp'].dt.date >= date_range[0]) & 
    (orders_df['order_purchase_timestamp'].dt.date <= date_range[1])
]

if selected_state != 'Semua':
    filtered_customers = customers_df[customers_df['customer_state'] == selected_state]
    filtered_orders = filtered_orders[filtered_orders['customer_id'].isin(filtered_customers['customer_id'])]

# Menggabungkan pesanan yang sudah difilter dengan order items
filtered_order_items = order_items_df[order_items_df['order_id'].isin(filtered_orders['order_id'])]

if selected_category != 'Semua':
    filtered_products = products_df[products_df['product_category_name'] == selected_category]
    filtered_order_items = filtered_order_items[filtered_order_items['product_id'].isin(filtered_products['product_id'])]

# Menghitung total pendapatan dari pesanan yang sudah difilter
filtered_payments = order_payments_df[order_payments_df['order_id'].isin(filtered_orders['order_id'])]

# ============================
# TAB ANALISIS
# ============================

# time loader
import time
my_bar = st.progress(0)
for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1)


tab1, tab2, tab3, tab4 = st.tabs([
    "📌 Produk Populer", 
    "💳 Metode Pembayaran", 
    "⭐ Kategori Produk Berdasarkan Review", 
    "🏙️ Transaksi per Kota"
])

# Tab 1: Produk Terpopuler
with tab1:
    st.header("Produk yang Paling Sering Dibeli")
    
    # Menggabungkan order items dengan produk berdasarkan pesanan yang sudah difilter
    product_counts = pd.merge(filtered_order_items, products_df, on='product_id')
    
    # Menghitung jumlah transaksi per kategori produk
    product_popularity = product_counts['product_category_name'].value_counts().reset_index()
    product_popularity.columns = ['product_category_name', 'total_orders']
    
    # Mengurutkan berdasarkan jumlah transaksi terbanyak
    product_popularity = product_popularity.sort_values(by='total_orders', ascending=False).head(10)

    # Visualisasi
    fig = px.bar(
        product_popularity, 
        x='total_orders', 
        y='product_category_name', 
        orientation='h',
        title="10 Kategori Produk Terpopuler"
    )
    fig.update_layout(xaxis_title="Jumlah Pembelian", yaxis_title="Kategori Produk", yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig)

# Tab 2: Metode Pembayaran Terpopuler
with tab2:
    st.header("Metode Pembayaran yang Paling Sering Digunakan")
    payment_counts = filtered_payments['payment_type'].value_counts()
    fig = px.pie(values=payment_counts.values, names=payment_counts.index, title="Distribusi Metode Pembayaran")
    st.plotly_chart(fig)

# Tab 3: Kategori Produk Berdasarkan Review
with tab3:
    st.header("Kategori Produk Berdasarkan Review")
    
    # Menggabungkan data review dengan pesanan dan produk
    filtered_reviews = order_reviews_df[order_reviews_df['order_id'].isin(filtered_orders['order_id'])]
    satisfaction_df = pd.merge(filtered_reviews, filtered_order_items, on='order_id')
    satisfaction_df = pd.merge(satisfaction_df, products_df, on='product_id')
    
    # Hitung rata-rata skor ulasan per kategori produk
    avg_satisfaction = satisfaction_df.groupby('product_category_name')['review_score'].mean().sort_values(ascending=False).head(10)
    
    # Visualisasi hasil
    fig = px.bar(x=avg_satisfaction.index, y=avg_satisfaction.values, title="Kategori Produk dengan Review Terbaik")
    fig.update_layout(xaxis_title="Kategori Produk", yaxis_title="Rata-rata Skor Review")
    st.plotly_chart(fig)

# Tab 4: Kota dengan Transaksi Terbanyak
with tab4:
    st.header("Kota dengan Jumlah Transaksi Terbanyak")
    filtered_customers = customers_df[customers_df['customer_id'].isin(filtered_orders['customer_id'])]
    city_counts = filtered_customers['customer_city'].value_counts().head(10)
    fig = px.bar(x=city_counts.index, y=city_counts.values, title="10 Kota dengan Transaksi Terbanyak")
    fig.update_layout(xaxis_title="Kota", yaxis_title="Jumlah Pelanggan")
    st.plotly_chart(fig)


