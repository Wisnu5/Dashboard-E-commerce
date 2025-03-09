import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
import time
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Load Data
@st.cache_data 
def load_data():
    return pd.read_csv("all_data.csv")

df = load_data()

# Sidebar Navigation
st.sidebar.title('🛒 E-Commerce Dashboard')
add_selectbox = st.sidebar.selectbox(
    'Pilih Analisis:',
    ('Produk Terlaris', 'Metode Pembayaran', 'Kategori Produk Terbaik', 'Kota dengan Transaksi Terbanyak')
)

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  bar.progress(i + 1)
  time.sleep(0.1)

# hide the placeholder
latest_iteration.empty()
bar.empty()

# Main Content
# produk terlaris
if add_selectbox == 'Produk Terlaris':
    st.title('📦 Produk Terlaris')
    # tampilkan nama produk yang paling sering dibeli
    st.write('Produk yang paling laris dibeli oleh pelanggan: ', df['product_id'].value_counts().idxmax())
    product_sales = df['product_id'].value_counts().head(10)
    fig = px.bar(product_sales, x=product_sales.index, y=product_sales.values, labels={'x':'Product ID', 'y':'Jumlah Terjual'}, color=product_sales.values, color_continuous_scale='Viridis')
    st.plotly_chart(fig)

# metode pembayaran
elif add_selectbox == 'Metode Pembayaran':
    st.title('💳 Metode Pembayaran')
    payment_method = df['payment_type'].value_counts()
    fig = px.pie(payment_method, values=payment_method.values, names=payment_method.index, title='Pembayaran yang Paling Sering Digunakan')
    st.plotly_chart(fig)

# kategori produk terbaik
elif add_selectbox == 'Kategori Produk Terbaik':
    st.title('🏷️ Kategori Produk Terbaik')
    category_sales = df['product_category_name'].value_counts().head(10)
    fig = px.bar(category_sales, x=category_sales.index, y=category_sales.values, labels={'x':'Kategori Produk', 'y':'Jumlah Terjual'}, color=category_sales.values, color_continuous_scale='Viridis')
    st.plotly_chart(fig)

# kota dengan transaksi terbanyak
elif add_selectbox == 'Kota dengan Transaksi Terbanyak':
    st.title('🌆 Kota dengan Transaksi Terbanyak')
    city_sales = df['customer_city'].value_counts().head(10)
    fig = px.bar(city_sales, x=city_sales.index, y=city_sales.values, labels={'x':'Kota', 'y':'Jumah Transaksi'}, color=city_sales.values, color_continuous_scale='Viridis')
    st.plotly_chart(fig)

# # peta pelanggan Sao Paulo
# elif add_selectbox == 'Peta Pelanggan Sao Paulo':
#     st.title('🗺️ Peta Pelanggan Sao Paulo')
#     # filter data untuk kota Sao Paulo
#     sp_data = df[df['customer_city'] == 'sao paulo']
#     # buat peta
#     m = folium.Map(location=[-23.5505, -46.6333], zoom_start=10)
#     mc = MarkerCluster()
#     for idx, row in sp_data.iterrows():
#         mc.add_child(folium.Marker(location=[row['geolocation_lat'], row['geolocation_lng']], popup=row['customer_unique_id']))
#     m.add_child(mc)
#     folium_static(m)


# Footer
st.sidebar.markdown('Created by: Wisnu Al Hussaeni')