import streamlit as st
import pandas as pd
import re
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
    /* Thẻ so sánh sản phẩm */
    .compare-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 16px;
        height: 100%;
        text-align: center;
        display: flex;
        flex-direction: column;
    }
    .compare-card img {
        width: 80%;
        height: 150px;
        object-fit: cover;
        border-radius: 6px;
        margin-bottom: 16px;
        align-self: center;
    }
    .compare-card h5 {
        font-weight: 700;
        color: #0A488F;
        font-size: 1.1rem;
        margin-bottom: 12px;
        min-height: 44px; /* Đảm bảo chiều cao đồng nhất */
    }
    .compare-card hr {
        margin-top: auto; /* Đẩy đường kẻ xuống dưới */
        margin-bottom: 1rem;
    }
    .compare-card p {
        font-size: 0.95rem;
        color: #333;
    }
    /* Thẻ thông báo kết quả carbon được thiết kế lại */
    .carbon-info-box {
        background-color: #E8F5E9; /* Nền xanh lá nhạt */
        color: #1B5E20; /* Chữ xanh lá đậm */
        border: 1px solid #A5D6A7;
        border-radius: 8px;
        padding: 15px;
        margin-top: 15px;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# --- HÀM HỖ TRỢ ---
def get_image_as_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except (FileNotFoundError, Exception):
        return None

def parse_emission(value):
    """Hàm xử lý chuỗi hệ số phát thải và trả về một số."""
    try:
        he_so_str = str(value)
        match = re.match(r'^[0-9.\-–]+', he_so_str)
        if not match: return None
        clean_str = match.group(0).replace('–', '-')
        if '-' in clean_str:
            low, high = map(float, clean_str.split('-'))
            return (low + high) / 2
        else:
            return float(clean_str)
    except: return None

@st.cache_data
def load_products():
    try:
        return pd.read_csv("data/products.csv", encoding='utf-8')
    except FileNotFoundError:
        st.error("Không tìm thấy file 'products.csv' trong thư mục 'data'.")
        return pd.DataFrame()

# --- GIAO DIỆN CHÍNH ---
st.title("Công cụ Hỗ trợ Ra quyết định 🛠️")
st.write("Sử dụng các công cụ so sánh và ước tính để lựa chọn vật liệu tối ưu cho dự án của bạn.")

products_df = load_products()

if not products_df.empty:
    product_list = products_df['Ten_san_pham'].tolist()

    # --- CÔNG CỤ SO SÁNH SẢN PHẨM ---
    with st.container():
        st.subheader("So sánh Sản phẩm")
        st.markdown("Chọn hai hoặc ba sản phẩm để so sánh các thông số kỹ thuật và chứng nhận.")
        
        compare_products = st.multiselect(
            "Chọn sản phẩm để so sánh:",
            options=product_list,
            max_selections=3
        )

        if len(compare_products) >= 2:
            comparison_df = products_df[products_df['Ten_san_pham'].isin(compare_products)]
            cols = st.columns(len(compare_products))

            for i, product_name in enumerate(compare_products):
                with cols[i]:
                    product_data = comparison_df[comparison_df['Ten_san_pham'] == product_name].iloc[0]
                    image_path = Path(f"images/{product_data['Link_Hinh_anh']}")
                    img_base64 = get_image_as_base64(image_path)
                    
                    img_html = (f'<img src="data:image/png;base64,{img_base64}" alt="{product_data["Ten_san_pham"]}">' if img_base64 
                                else '<div style="height: 150px; display:flex; align-items:center; justify-content:center; background-color:#f0f2f6; border-radius:6px;">No Image</div>')

                    st.markdown(f"""
                    <div class="compare-card">
                        {img_html}
                        <h5>{product_data['Ten_san_pham']}</h5>
                        <hr>
                        <p><strong>Loại vật liệu:</strong><br>{product_data['Loai_vat_lieu']}</p>
                        <p><strong>Chứng nhận:</strong><br>{product_data['Chung_nhan']}</p>
                        <p><strong>Hệ số phát thải:</strong><br>{product_data['He_so_phat_thai']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- CÔNG CỤ ƯỚC TÍNH "DẤU CHÂN CARBON" ---
    with st.container(border=True):
        st.subheader("Ước tính Dấu chân Carbon")
        st.markdown("Ước tính sơ bộ lượng phát thải CO2 của vật liệu dựa trên diện tích sử dụng.")

        col1, col2 = st.columns(2)
        with col1:
            selected_product_carbon = st.selectbox("Chọn vật liệu cần ước tính:", options=product_list)
        with col2:
            area = st.number_input("Nhập diện tích sử dụng (m²):", min_value=1.0, value=100.0, step=10.0)

        if st.button("Ước tính ngay", type="primary", use_container_width=True):
            product_info = products_df[products_df['Ten_san_pham'] == selected_product_carbon].iloc[0]
            he_so_value = product_info['He_so_phat_thai']
            he_so_numeric = parse_emission(he_so_value)

            if he_so_numeric is not None:
                total_co2 = area * he_so_numeric
                trees_equivalent = total_co2 / 22 
                
                st.metric(label="Tổng phát thải CO2 ước tính", value=f"{total_co2:.2f} kg CO2")
                
                # SỬA LỖI: Sử dụng thẻ div tùy chỉnh thay cho st.info
                st.markdown(f"""
                <div class="carbon-info-box">
                    💡 Con số này tương đương với lượng CO2 mà khoảng <strong>{trees_equivalent:.1f} cây xanh</strong> hấp thụ trong một năm.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"Không thể tính toán. Dữ liệu hệ số phát thải '{he_so_value}' không hợp lệ hoặc không có.")
else:
    st.info("Vui lòng tải lên file 'products.csv' để sử dụng các công cụ.")

