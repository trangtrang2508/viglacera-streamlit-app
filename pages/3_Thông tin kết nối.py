import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import math
import base64
from pathlib import Path

# --- SIDEBAR ---
# Sử dụng with st.sidebar để thêm nội dung vào thanh bên trái
with st.sidebar:
    # Bạn có thể thay thế link này bằng đường dẫn tới logo của bạn trong thư mục /images
    st.image("images/download.png", use_container_width=True)
    st.title("Về Viglacera Xanh")
    st.markdown("""
    **Cổng thông tin VLXD Xanh** là một sáng kiến của Viglacera nhằm cung cấp kiến thức và công cụ để hỗ trợ các dự án xây dựng bền vững tại Việt Nam.
    """)
    st.divider()
    st.markdown("🔗 **Liên kết hữu ích**")
    # Link đến trang web chính thức của Viglacera
    st.link_button("Trang chủ Viglacera 🏠", "https://viglacera.com.vn/", use_container_width=True)
    # Link đến trang liên hệ trong ứng dụng của bạn
    st.page_link("pages/4_Tương tác hỗ trợ.py", label="Liên hệ chúng tôi ✉️", use_container_width=True)

# --- CSS TÙY CHỈNH CHO GIAO DIỆN ---
st.markdown("""
<style>
    /* Thẻ bài viết trong thư viện tri thức */
    .article-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 0; /* Xóa padding cũ để ảnh vừa khít */
        height: 100%; /* Đảm bảo các thẻ trên cùng một hàng bằng nhau */
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: box-shadow 0.3s ease-in-out;
        display: flex;
        flex-direction: column;
        overflow: hidden; /* Ẩn phần thừa của ảnh */
    }
    .article-card:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
    }
    .article-card img {
        width: 100%;
        height: 150px; /* Chiều cao cố định cho ảnh */
        object-fit: cover; /* Đảm bảo ảnh lấp đầy mà không bị méo */
    }
    .article-content {
        padding: 20px;
        display: flex;
        flex-direction: column;
        flex-grow: 1; /* Quan trọng: giúp thẻ co giãn bằng nhau */
    }
    .article-card h5 {
        font-weight: 700;
        color: #0A488F;
        margin-top: 0;
        min-height: 50px;
        /* Giới hạn 2 dòng cho tiêu đề */
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .article-card p {
        font-size: 0.95rem;
        color: #333;
        flex-grow: 1; /* Đẩy link xuống dưới cùng */
        /* Giới hạn 3 dòng cho tóm tắt */
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .article-card a {
        text-decoration: none;
        color: #00A99D;
        font-weight: 600;
        margin-top: 15px;
    }
    /* Thẻ giữ chỗ trống */
    .placeholder-card {
        background-color: transparent;
        border: 1px dashed #d0d0d0;
        border-radius: 10px;
        height: 100%;
        min-height: 350px; /* Chiều cao tối thiểu để bằng các thẻ khác */
    }
    /* Các nút bấm (giữ nguyên) */
    .stButton>button { border-radius: 8px; padding: 8px 16px; border: 1px solid #0A488F; background-color: #FFFFFF; color: #0A488F; transition: all 0.3s ease; font-weight: 600; }
    .stButton>button:hover { background-color: #F0F2F6; border-color: #00A99D; color: #00A99D; }
    .stButton>button[kind="primary"] { background-color: #0A488F; color: #FFFFFF; border: none; }
    .stButton>button[kind="primary"]:hover { background-color: #00A99D; }
</style>
""", unsafe_allow_html=True)


# --- HÀM HỖ TRỢ ---
@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path, encoding='utf-8')
    except FileNotFoundError:
        st.error(f"Không tìm thấy file '{file_path}'. Vui lòng kiểm tra lại.")
        return pd.DataFrame()

def get_image_as_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except (FileNotFoundError, Exception):
        return None

# --- GIAO DIỆN CHÍNH ---
st.title("Thông tin và Kết nối 🌐")
st.write("Tìm kiếm nhà cung ứng, phân phối và mở rộng kiến thức với thư viện tri thức của chúng tôi.")

# --- BẢN ĐỒ NHÀ CUNG ỨNG/PHÂN PHỐI ---
st.subheader("Bản đồ Nhà cung ứng và Phân phối")
suppliers_df = load_data("data/suppliers.csv")

if not suppliers_df.empty:
    with st.container():
        col1, col2 = st.columns([1, 2])
        # ... (Phần code bản đồ giữ nguyên) ...
        with col1:
            st.markdown("##### Bộ lọc và Danh sách")
            if 'Tinh_Thanh' in suppliers_df.columns:
                unique_cities = ["Tất cả"] + sorted(suppliers_df['Tinh_Thanh'].dropna().unique().tolist())
                selected_city = st.selectbox("Chọn Tỉnh/Thành phố:", unique_cities)
                
                if selected_city == "Tất cả":
                    filtered_suppliers = suppliers_df
                else:
                    filtered_suppliers = suppliers_df[suppliers_df['Tinh_Thanh'] == selected_city]
            else:
                st.warning("Thiếu cột 'Tinh_Thanh' trong suppliers.csv để lọc.")
                filtered_suppliers = suppliers_df
            
            with st.container(height=400, border=False):
                for index, row in filtered_suppliers.iterrows():
                    st.markdown(f"**{row['Ten_nha_cung_ung']}**\n\n📍 {row['Dia_chi']}")
                    st.divider()
        with col2:
            if not filtered_suppliers.empty:
                map_center = [filtered_suppliers['Vi_do'].mean(), filtered_suppliers['Kinh_do'].mean()]
                zoom_start = 9 if selected_city != "Tất cả" else 6
                m = folium.Map(location=map_center, zoom_start=zoom_start)
                
                for index, row in filtered_suppliers.iterrows():
                    folium.Marker(
                        location=[row['Vi_do'], row['Kinh_do']],
                        popup=f"<b>{row['Ten_nha_cung_ung']}</b><br>{row['Dia_chi']}",
                        tooltip=row['Ten_nha_cung_ung']
                    ).add_to(m)
                
                st_folium(m, width=700, height=450)
            else:
                st.info("Không có nhà cung ứng nào phù hợp với bộ lọc.")
else:
    st.info("Không có dữ liệu nhà cung ứng để hiển thị bản đồ.")

st.markdown("<br><br>", unsafe_allow_html=True)

# --- THƯ VIỆN TRI THỨC (GIAO DIỆN MỚI CÓ HÌNH ẢNH) ---
articles_df = load_data("data/articles.csv")

if not articles_df.empty:
    if 'article_page' not in st.session_state:
        st.session_state.article_page = 0
    if 'view_all_articles' not in st.session_state:
        st.session_state.view_all_articles = False

    # --- Header và các nút điều khiển ---
    header_cols = st.columns([0.5, 0.5])
    with header_cols[0]:
        st.subheader("Thư viện Tri thức")
        st.write("Các bài viết chuyên sâu về VLXD xanh.")
    
    with header_cols[1]:
        control_cols = st.columns(3)
        button_text = "Thu gọn" if st.session_state.view_all_articles else "Xem tất cả"
        if control_cols[2].button(button_text, use_container_width=True, key="toggle_view", type="primary"):
            st.session_state.view_all_articles = not st.session_state.view_all_articles
            st.session_state.article_page = 0

        if not st.session_state.view_all_articles:
            if control_cols[0].button("◀ Trước", use_container_width=True, key="prev_article"):
                st.session_state.article_page = max(0, st.session_state.article_page - 1)
            if control_cols[1].button("Sau ▶", use_container_width=True, key="next_article"):
                num_pages = math.ceil(len(articles_df) / 3)
                st.session_state.article_page = min(num_pages - 1, st.session_state.article_page + 1)
    st.divider()

    # --- Hàm để hiển thị một thẻ bài viết ---
    def render_article_card(row):
        image_path = Path(f"images/{row['Link_Hinh_anh']}")
        img_base64 = get_image_as_base64(image_path)
        img_html = (f'<img src="data:image/png;base64,{img_base64}" alt="{row["Tieu_de"]}">' if img_base64 
                    else '<div style="height: 150px; display:flex; align-items:center; justify-content:center; background-color:#f0f2f6;">No Image</div>')

        return f"""
        <div class="article-card">
            {img_html}
            <div class="article-content">
                <h5>{row['Tieu_de']}</h5>
                <p>{row['Tom_tat']}</p>
                <a href="{row['Link_bai_viet']}" target="_blank">Đọc bài viết đầy đủ →</a>
            </div>
        </div>
        """

    # --- Hiển thị nội dung ---
    if st.session_state.view_all_articles:
        num_articles = len(articles_df)
        cols = st.columns(3)
        for i in range(num_articles):
            with cols[i % 3]:
                st.markdown(render_article_card(articles_df.iloc[i]), unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        start_index = st.session_state.article_page * 3
        end_index = start_index + 3
        articles_on_page = articles_df.iloc[start_index:end_index]
        
        cols = st.columns(3)
        for i in range(3):
            if i < len(articles_on_page):
                with cols[i]:
                    st.markdown(render_article_card(articles_on_page.iloc[i]), unsafe_allow_html=True)
            else:
                with cols[i]:
                    st.markdown('<div class="placeholder-card"></div>', unsafe_allow_html=True)
else:
    st.info("Chưa có bài viết nào trong thư viện tri thức.")

