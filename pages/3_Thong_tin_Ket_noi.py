# pages/3_Thong_tin_Ket_noi.py
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("Thông tin và Kết nối 🌐")
st.write("Tìm kiếm nhà cung ứng, phân phối và mở rộng kiến thức với thư viện tri thức của chúng tôi.")

# --- Bản đồ nhà cung ứng/phân phối ---
st.subheader("Bản đồ Nhà cung ứng/Phân phối")

@st.cache_data
def load_suppliers():
    try:
        return pd.read_csv("data/suppliers.csv")
    except FileNotFoundError:
        st.error("Không tìm thấy file 'suppliers.csv' trong thư mục 'data'.")
        return pd.DataFrame()

suppliers_df = load_suppliers()

if not suppliers_df.empty:
    map_center = [suppliers_df['Vi_do'].mean(), suppliers_df['Kinh_do'].mean()]
    m = folium.Map(location=map_center, zoom_start=7)
    for index, row in suppliers_df.iterrows():
        folium.Marker(
            location=[row['Vi_do'], row['Kinh_do']],
            popup=f"<b>{row['Ten_nha_cung_ung']}</b><br>{row['Dia_chi']}",
            tooltip=row['Ten_nha_cung_ung']
        ).add_to(m)
    st_folium(m, width=700, height=400)
else:
    st.info("Không có dữ liệu nhà cung ứng để hiển thị bản đồ.")

st.markdown("---")

# --- Thư viện tri thức (Đọc từ file CSV) ---
st.subheader("Thư viện Tri thức")
st.write("Các bài viết chuyên sâu, hướng dẫn kỹ thuật và dự án thực tế về VLXD xanh.")

@st.cache_data
def load_articles():
    try:
        return pd.read_csv("data/articles.csv")
    except FileNotFoundError:
        st.error("Không tìm thấy file 'articles.csv' trong thư mục 'data'. Vui lòng tạo file và thêm nội dung.")
        return pd.DataFrame()

articles_df = load_articles()

if not articles_df.empty:
    for index, row in articles_df.iterrows():
        with st.expander(f"#### {row['Tieu_de']}"):
            st.write(f"**Tóm tắt:** {row['Tom_tat']}")
            # Thêm link có thể bấm vào được
            st.markdown(f"**[Đọc bài viết đầy đủ]({row['Link_bai_viet']})**")
else:
    st.info("Chưa có bài viết nào trong thư viện tri thức. Vui lòng thêm vào file articles.csv.")