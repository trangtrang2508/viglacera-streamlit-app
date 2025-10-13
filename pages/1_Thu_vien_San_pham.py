# pages/1_Thu_vien_San_pham.py
import streamlit as st
import pandas as pd

# THÊM ĐOẠN CSS NÀY VÀO ĐÂY
st.markdown("""
<style>
/* CSS để ép các dòng chữ dài phải tự xuống hàng */
.st-emotion-cache-1y4p8pa { 
    word-wrap: break-word;
}
</style>
""", unsafe_allow_html=True)

st.title("Thư viện Sản phẩm Xanh 🌿")
st.write("Khám phá danh mục các vật liệu xây dựng xanh của Viglacera với các bộ lọc thông minh.")

@st.cache_data # Streamlit sẽ cache dữ liệu để không load lại mỗi lần thay đổi
def load_products():
    try:
        return pd.read_csv("data/products.csv")
    except FileNotFoundError:
        st.error("Không tìm thấy file 'products.csv' trong thư mục 'data'. Vui lòng kiểm tra lại.")
        return pd.DataFrame()

products_df = load_products()

if not products_df.empty:
    # --- Bộ lọc nâng cao ---
    st.subheader("Bộ lọc sản phẩm")
    col1, col2, col3 = st.columns(3)

    with col1:
        # Lọc theo loại vật liệu (lấy các giá trị duy nhất từ cột Loai_vat_lieu)
        unique_loai = products_df["Loai_vat_lieu"].unique().tolist()
        loai_vat_lieu_selected = st.multiselect(
            "Lọc theo loại vật liệu:",
            options=unique_loai,
            default=[]
        )

    with col2:
        # Lọc theo chứng nhận (cần xử lý chuỗi nếu có nhiều chứng nhận)
        all_certs = []
        for cert_str in products_df["Chung_nhan"].dropna():
            all_certs.extend([c.strip() for c in cert_str.split(',')])
        unique_certs = sorted(list(set(all_certs)))
        chung_nhan_selected = st.multiselect(
            "Lọc theo chứng nhận:",
            options=unique_certs,
            default=[]
        )

    with col3:
        # Thanh tìm kiếm thông minh theo tên sản phẩm hoặc mô tả
        search_query = st.text_input("Tìm kiếm theo tên hoặc mô tả sản phẩm:")

    # --- Áp dụng bộ lọc và tìm kiếm ---
    filtered_df = products_df.copy()

    if loai_vat_lieu_selected:
        filtered_df = filtered_df[filtered_df["Loai_vat_lieu"].isin(loai_vat_lieu_selected)]

    if chung_nhan_selected:
        # Lọc sản phẩm có ít nhất một chứng nhận được chọn
        filtered_df = filtered_df[
            filtered_df["Chung_nhan"].apply(
                lambda x: any(c.strip() in chung_nhan_selected for c in str(x).split(','))
            )
        ]

    if search_query:
        filtered_df = filtered_df[
            filtered_df["Ten_san_pham"].str.contains(search_query, case=False, na=False) |
            filtered_df["Mo_ta_ngan"].str.contains(search_query, case=False, na=False)
        ]

    st.markdown("---")
    st.subheader(f"Kết quả tìm kiếm ({len(filtered_df)} sản phẩm):")

    # --- Hiển thị danh sách sản phẩm ---
    if filtered_df.empty:
        st.warning("Không tìm thấy sản phẩm nào phù hợp với tiêu chí lọc.")
    else:
        for index, row in filtered_df.iterrows():
            # Sử dụng st.expander để tạo trang chi tiết sản phẩm thu gọn
            with st.expander(f"### {row['Ten_san_pham']} - ID: {row['ID']}"):
                col_img, col_info = st.columns([1, 2])
                with col_img:
                    if pd.notna(row['Link_Hinh_anh']):
                        st.image(f"images/{row['Link_Hinh_anh']}", width=250, caption=row['Ten_san_pham'])
                    else:
                        st.image("https://via.placeholder.com/250x200?text=No+Image", width=250)
                with col_info:
                    st.write(f"**Mô tả:** {row['Mo_ta_ngan']}")
                    st.write(f"**Loại vật liệu:** {row['Loai_vat_lieu']}")
                    st.write(f"**Chứng nhận:** {row['Chung_nhan']}")
                    st.write(f"**Hệ số phát thải:** {row['He_so_phat_thai']} kg CO2/m² (ước tính)")
                    st.markdown(f"**Tải tài liệu:**")
                    # Kiểm tra xem có link PDF hoặc link BIM/CAD hay không
                    has_pdf = pd.notna(row['Link_PDF']) and row['Link_PDF'] != 'N/A'
                    has_bim_cad = 'Link_BIM_CAD' in row and pd.notna(row['Link_BIM_CAD']) and row['Link_BIM_CAD'] != 'N/A'
                    # Chỉ hiển thị link nếu có
                    if has_pdf:
                        st.markdown(f"- [Tài liệu kỹ thuật (PDF)]({row['Link_PDF']})")
                    if has_bim_cad:
                        st.markdown(f"- [Mô hình BIM/CAD]({row['Link_BIM_CAD']})")
                    # Chỉ thông báo khi không có bất kỳ tài liệu nào
                    if not has_pdf and not has_bim_cad:
                        st.info("Chưa có tài liệu PDF/BIM/CAD.")
else:
    st.info("Vui lòng tải lên file 'products.csv' để xem thư viện sản phẩm.")