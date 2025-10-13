# pages/2_Cong_cu_Ho_tro.py
import streamlit as st
import pandas as pd
import re #

st.title("Công cụ Hỗ trợ Ra quyết định 🛠️")
st.write("Sử dụng các công cụ so sánh và ước tính để lựa chọn vật liệu tối ưu cho dự án của bạn.")

@st.cache_data
def load_products():
    try:
        return pd.read_csv("data/products.csv")
    except FileNotFoundError:
        st.error("Không tìm thấy file 'products.csv' trong thư mục 'data'.")
        return pd.DataFrame()

products_df = load_products()

if not products_df.empty:
    product_list = products_df['Ten_san_pham'].tolist()

    # --- Công cụ so sánh sản phẩm ---
    st.subheader("Công cụ So sánh Sản phẩm")
    st.markdown("Chọn hai hoặc ba sản phẩm để so sánh các thông số kỹ thuật và chứng nhận.")

    compare_products = st.multiselect(
        "Chọn sản phẩm để so sánh:",
        options=product_list,
        max_selections=3, # Cho phép so sánh tối đa 3 sản phẩm
        key="compare_selector"
    )

    if len(compare_products) >= 2:
        comparison_df = products_df[products_df['Ten_san_pham'].isin(compare_products)]
        # Chọn các cột quan trọng để hiển thị khi so sánh
        display_cols = ['Ten_san_pham', 'Loai_vat_lieu', 'Chung_nhan', 'He_so_phat_thai', 'Mo_ta_ngan']
        st.table(comparison_df[display_cols].T.reset_index().rename(columns={'index': 'Thông số'}))
    elif len(compare_products) == 1:
        st.info("Vui lòng chọn ít nhất hai sản phẩm để so sánh.")
    else:
        st.info("Chọn sản phẩm từ danh sách trên để bắt đầu so sánh.")


    st.markdown("---")

    # --- Công cụ ước tính "Dấu chân carbon" ---
    st.subheader("Công cụ Ước tính Dấu chân Carbon")
    st.markdown("Ước tính sơ bộ lượng phát thải CO2 của vật liệu dựa trên diện tích sử dụng.")

    selected_product_carbon = st.selectbox(
        "Chọn vật liệu cần ước tính:",
        options=product_list,
        key="carbon_selector"
    )
    area = st.number_input(
        "Nhập diện tích sử dụng (m²):",
        min_value=1.0,
        value=100.0,
        step=10.0,
        key="area_input"
    )

    if st.button("Ước tính Dấu chân Carbon", key="calculate_carbon"):
        product_info = products_df[products_df['Ten_san_pham'] == selected_product_carbon]
        if not product_info.empty:
            he_so_value = product_info['He_so_phat_thai'].iloc[0]

            if pd.notna(he_so_value):
                try:
                    he_so_numeric = 0
                    he_so_str = str(he_so_value).strip() # Chuyển thành chuỗi và xóa khoảng trắng thừa

                    # Bước 1: Chỉ trích xuất phần số và dấu gạch ở đầu chuỗi
                    match = re.match(r'^[0-9.\-–]+', he_so_str)
                    if not match:
                        raise ValueError("Không tìm thấy dữ liệu số hợp lệ.")

                    clean_str = match.group(0)

                    # Bước 2: Chuẩn hóa các loại dấu gạch ngang thành 1 loại duy nhất
                    normalized_str = clean_str.replace('–', '-')

                    # Bước 3: Tính toán như cũ với chuỗi đã được làm sạch
                    if '-' in normalized_str:
                        parts = normalized_str.split('-')
                        if len(parts) != 2: # Đảm bảo chỉ có 2 phần
                            raise ValueError("Khoảng số không hợp lệ.")
                        low, high = map(float, parts)
                        he_so_numeric = (low + high) / 2
                        st.info(f"Hệ số phát thải là một khoảng ({clean_str}). Tạm tính giá trị trung bình là {he_so_numeric:.2f} để ước tính.")
                    else:
                        he_so_numeric = float(normalized_str)

                    # Thực hiện phép tính
                    total_co2 = area * he_so_numeric
                    st.success(f"**Lượng phát thải CO2 ước tính cho {area} m² {selected_product_carbon}:** **{total_co2:.2f} kg CO2**")
                    st.info("Lưu ý: Đây là ước tính sơ bộ. Để có con số chính xác, vui lòng tham khảo tài liệu kỹ thuật chi tiết.")

                except (ValueError, TypeError):
                    st.warning(f"Không thể tính toán. Dữ liệu hệ số phát thải '{he_so_value}' không hợp lệ.")
            else:
                st.warning("Không có hệ số phát thải cho sản phẩm này.")
        else:
            st.error("Sản phẩm không hợp lệ.")

else:
    st.info("Vui lòng tải lên file 'products.csv' để sử dụng các công cụ.")