# app.py
import streamlit as st

# Cấu hình trang (tiêu đề, icon, layout)
st.set_page_config(
    page_title="Viglacera VLXD Xanh",
    page_icon="🌱",
    layout="wide", # Có thể là "centered" hoặc "wide"
    initial_sidebar_state="expanded" # Để sidebar mở mặc định
)

# Tiêu đề chính của trang chủ
st.title("Chào mừng đến với Cổng thông tin Vật liệu Xây dựng Xanh Viglacera 🌱")

# Hình ảnh minh họa (thay thế URL ảnh nếu có ảnh thật)
st.image("https://via.placeholder.com/900x400/008000/FFFFFF?text=Viglacera+Green+Building+Materials", use_container_width=True)

# Đoạn giới thiệu
st.write(
    """
    Nền tảng cung cấp thông tin minh bạch và đáng tin cậy về các sản phẩm Vật liệu Xây dựng Xanh (VLXD Xanh)
    của Viglacera, hỗ trợ bạn đưa ra quyết định xây dựng bền vững và hiệu quả.

    Chúng tôi cam kết mang đến những giải pháp vật liệu tiên tiến, thân thiện môi trường,
    đáp ứng các tiêu chuẩn khắt khe nhất về bền vững.

    Sử dụng menu bên trái để khám phá các tính năng của cổng thông tin!
    """
)

st.markdown("---") # Đường phân cách
st.subheader("Về Viglacera và Cam kết Xanh")
st.write(
    """
    Viglacera tự hào là doanh nghiệp tiên phong trong lĩnh vực sản xuất VLXD xanh tại Việt Nam.
    Với kinh nghiệm và hệ thống nhà máy hiện đại, chúng tôi không ngừng nghiên cứu và phát triển
    các sản phẩm chất lượng cao, giảm thiểu tác động đến môi trường.
    """
)
st.info("Tìm hiểu thêm về Viglacera tại trang Giới thiệu & Liên hệ.")