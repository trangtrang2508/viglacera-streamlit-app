import streamlit as st
import pandas as pd
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

# --- HÀM HỖ TRỢ VÀ CALLBACK ---
def get_image_as_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except (FileNotFoundError, Exception):
        return None

def go_back_to_library():
    """Hàm callback để xóa query param và quay lại thư viện."""
    st.query_params.clear()

# --- CSS TÙY CHỈNH CHO CẢ HAI GIAO DIỆN ---
st.markdown("""
<style>
    /* Giao diện thẻ sản phẩm trong lưới */
    .product-card {
        background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px;
        padding: 16px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
        height: 100%; 
        display: flex; 
        flex-direction: column;
        min-height: 450px; 
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 8px 16px rgba(0,0,0,0.1); }
    .product-card img { width: 100%; height: 180px; object-fit: cover; border-radius: 6px; margin-bottom: 16px; }
    
    /* --- THAY ĐỔI MÀU SẮC Ở ĐÂY --- */
    .product-card h5 {
        font-weight: 700; 
        color: #55853d; /* Đổi sang màu xanh Google */
        font-size: 1.1rem; margin-bottom: 8px;
        display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
        overflow: hidden; text-overflow: ellipsis; 
        min-height: 2.5em; 
    }

    .product-card p {
        color: #555555; font-size: 0.9rem; 
        flex-grow: 1;
        display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
        overflow: hidden; text-overflow: ellipsis;
    }

    /* --- THAY ĐỔI MÀU SẮC Ở ĐÂY --- */
    .view-details-button {
        display: block; padding: 10px 18px; 
        background-color: #55853d; /* Đổi sang màu xanh Google */
        color: white !important;
        text-align: center; border-radius: 5px; text-decoration: none; margin-top: 16px;
        font-weight: 600; transition: background-color 0.3s ease;
    }
    .view-details-button:hover { 
        background-color: #1a73e8; /* Đổi sang màu xanh Google đậm hơn */
        color: white !important; 
    }
    
    /* Giao diện trang chi tiết sản phẩm */
    .product-detail-image { border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    
    /* CSS Mới cho nút tải xuống */
    .stDownloadButton>button {
        width: 100%;
        background-color: #F0F2F6;
        color: #31333F;
        border: 1px solid #E0E0E0;
        font-weight: 600;
    }
    .stDownloadButton>button:hover {
        background-color: #E0E0E0;
        border-color: #BDBDBD;
        color: #31333F;
    }
</style>
""", unsafe_allow_html=True)


# --- HÀM TẢI DỮ LIỆU ---
@st.cache_data
def load_products():
    try:
        return pd.read_csv("data/products.csv", encoding='utf-8')
    except FileNotFoundError:
        st.error("Không tìm thấy file 'products.csv' trong thư mục 'data'.")
        return pd.DataFrame()

products_df = load_products()

# --- HÀM HIỂN THỊ TRANG CHI TIẾT SẢN PHẨM ---
def display_product_details(product_id):
    product = products_df[products_df['ID'] == product_id].iloc[0]

    st.button("⬅️ Quay lại Thư viện sản phẩm", on_click=go_back_to_library)
    
    st.title(product["Ten_san_pham"])
    st.markdown("---")

    col1, col2 = st.columns([2, 3])

    with col1:
        image_path = Path(f"images/{product['Link_Hinh_anh']}")
        img_base64 = get_image_as_base64(image_path)

        if img_base64:
            st.markdown(f'''
                <img src="data:image/png;base64,{img_base64}" alt="{product["Ten_san_pham"]}" class="product-detail-image" style="width: 100%;">
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
                <img src="https://via.placeholder.com/400x400/F0F2F6/31333F?text=No+Image" alt="Image not available" class="product-detail-image" style="width: 100%;">
            ''', unsafe_allow_html=True)
        st.caption(product["Ten_san_pham"])


    with col2:
        st.subheader("Mô tả chi tiết")
        st.write(product["Mo_ta_ngan"])

        st.subheader("Thông số kỹ thuật")
        st.markdown(f"""
        - **Loại vật liệu:** {product['Loai_vat_lieu']}
        - **Chứng nhận:** {product['Chung_nhan']}
        - **Hệ số phát thải:** {product['He_so_phat_thai']}
        """)
        
        # --- BẮT ĐẦU PHẦN THAY ĐỔI ---
        st.subheader("Tài liệu")
        
        pdf_filename = product['Link_PDF'] if pd.notna(product['Link_PDF']) else None
        bim_link = product['Link_BIM_CAD'] if 'Link_BIM_CAD' in product and pd.notna(product['Link_BIM_CAD']) else None
        
        has_downloads = False
        dl_col1, dl_col2 = st.columns(2)

        # Xử lý nút tải PDF từ file cục bộ
        if pdf_filename:
            pdf_path = Path(f"pdf/{pdf_filename}")
            if pdf_path.is_file():
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                dl_col1.download_button(
                    label="📄 Tải PDF",
                    data=pdf_bytes,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    use_container_width=True
                )
                has_downloads = True
        
        # Giữ nguyên nút link cho BIM/CAD (vì thường là link ngoài)
        if bim_link:
            dl_col2.link_button("📦 Tải BIM/CAD", url=bim_link, use_container_width=True)
            has_downloads = True
            
        if not has_downloads:
            st.info("Chưa có tài liệu để tải về.")
        # --- KẾT THÚC PHẦN THAY ĐỔI ---


# --- HÀM HIỂN THỊ LƯỚI SẢN PHẨM ---
def display_product_grid(df):
    if df.empty:
        st.warning("Không tìm thấy sản phẩm nào phù hợp với tiêu chí của bạn.")
        return

    num_cols = 3
    cols = st.columns(num_cols)
    
    for i, row in df.iterrows():
        col = cols[i % num_cols]
        with col:
            details_link = f"?product_id={row['ID']}"
            image_path = Path(f"images/{row['Link_Hinh_anh']}")
            img_base64 = get_image_as_base64(image_path)
            
            img_html = (f'<img src="data:image/png;base64,{img_base64}" alt="{row["Ten_san_pham"]}">' if img_base64 
                        else f'<img src="https://via.placeholder.com/300x200/F0F2F6/31333F?text=No+Image" alt="{row["Ten_san_pham"]}">')

            st.markdown(f"""
            <div class="product-card">
                {img_html}
                <h5>{row["Ten_san_pham"]}</h5>
                <p>{row["Mo_ta_ngan"]}</p>
                <a href="{details_link}" target="_self" class="view-details-button">Xem chi tiết</a>
            </div>
            """, unsafe_allow_html=True)


# --- LOGIC CHÍNH: QUYẾT ĐỊNH HIỂN THỊ GIAO DIỆN NÀO ---
if "product_id" in st.query_params:
    try:
        selected_id = int(st.query_params["product_id"])
        display_product_details(selected_id)
    except (ValueError, IndexError, KeyError):
        st.error("Sản phẩm bạn tìm không tồn tại hoặc ID không hợp lệ.")
        st.button("⬅️ Quay lại Thư viện", on_click=go_back_to_library)
else:
    st.title("Thư viện Sản phẩm Xanh 🌿")
    st.write("Khám phá danh mục các vật liệu xây dựng xanh của Viglacera theo từng loại sản phẩm.")

    if not products_df.empty:
        st.subheader("Tìm kiếm và Lọc sản phẩm")
        col1, col2 = st.columns([2, 1])

        with col1:
            search_query = st.text_input("Tìm kiếm theo tên hoặc mô tả sản phẩm:")
        with col2:
            all_certs = []
            for cert_str in products_df["Chung_nhan"].dropna():
                all_certs.extend([c.strip() for c in cert_str.split(',')])
            unique_certs = sorted(list(set(all_certs)))
            chung_nhan_selected = st.multiselect("Lọc theo chứng nhận:", options=unique_certs)

        filtered_df = products_df.copy()
        if search_query:
            filtered_df = filtered_df[
                filtered_df["Ten_san_pham"].str.contains(search_query, case=False, na=False) |
                filtered_df["Mo_ta_ngan"].str.contains(search_query, case=False, na=False)
            ]
        if chung_nhan_selected:
            filtered_df = filtered_df[
                filtered_df["Chung_nhan"].apply(lambda x: any(c.strip() in chung_nhan_selected for c in str(x).split(',')))
            ]
        
        st.markdown("---")

        material_types = filtered_df['Loai_vat_lieu'].dropna().unique().tolist()
        tab_titles = ["Tất cả (" + str(len(filtered_df)) + ")"] + material_types
        tabs = st.tabs(tab_titles)

        for i, tab in enumerate(tabs):
            with tab:
                if i == 0:
                    display_product_grid(filtered_df)
                else:
                    material = material_types[i-1]
                    filtered_by_material = filtered_df[filtered_df['Loai_vat_lieu'] == material]
                    display_product_grid(filtered_by_material)
    else:
        st.info("Vui lòng tải lên file 'products.csv' để xem thư viện sản phẩm.")

