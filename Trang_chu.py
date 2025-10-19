import streamlit as st

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

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Viglacera VLXD Xanh",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS TÙY CHỈNH CHO GIAO DIỆN ---
st.markdown("""
<style>
    /* Link bao quanh thẻ */
    a.card-link {
        text-decoration: none; /* Bỏ gạch chân của link */
    }
    /* Thẻ tính năng */
    .feature-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%; /* Đảm bảo các thẻ có chiều cao bằng nhau */
    }
    a.card-link:hover .feature-card { /* Hiệu ứng khi di chuột vào link */
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }
    .feature-card .icon {
        font-size: 3rem;
        color: #00A99D; /* Màu xanh lá cây */
    }
    .feature-card h3 {
        color: #0A488F; /* Màu xanh dương */
        margin-top: 15px;
        font-size: 1.5rem;
    }
    .feature-card p {
        color: #31333F; 
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
col1, col2 = st.columns([0.6, 0.4])
with col1:
    st.title("Cổng thông tin Vật liệu Xây dựng Xanh Viglacera 🌱")
    st.write(
        """
        Nền tảng cung cấp thông tin minh bạch và đáng tin cậy về các sản phẩm Vật liệu Xây dựng Xanh (VLXD Xanh)
        của Viglacera, hỗ trợ bạn đưa ra quyết định xây dựng bền vững và hiệu quả.
        
        **Khám phá ngay các công cụ và tài nguyên hữu ích của chúng tôi!**
        """
    )
with col2:
    # --- THAY ĐỔI Ở ĐÂY ---
    # Thay thế URL bằng đường dẫn đến file ảnh cục bộ của bạn.
    # Hãy chắc chắn bạn có file "trang-chu-banner.png" trong thư mục "images".
    st.image("images/banner-phat-trien-ben-vung.jpg", use_container_width=True)

st.divider()

# --- CÁC TÍNH NĂNG CHÍNH ---
st.subheader("Khám phá Nền tảng")
cols = st.columns(3)
with cols[0]:
    st.markdown("""
    <a href="Thư viện sản phẩm" target="_self" class="card-link">
        <div class="feature-card">
            <div class="icon">📚</div>
            <h3>Thư viện Sản phẩm</h3>
            <p>Tra cứu thông tin chi tiết, thông số kỹ thuật và chứng nhận của hàng loạt sản phẩm VLXD Xanh.</p>
        </div>
    </a>
    """, unsafe_allow_html=True)

with cols[1]:
    st.markdown("""
    <a href="Công cụ hỗ trợ" target="_self" class="card-link">
        <div class="feature-card">
            <div class="icon">🛠️</div>
            <h3>Công cụ Hỗ trợ</h3>
            <p>So sánh các sản phẩm và ước tính dấu chân carbon để đưa ra lựa chọn vật liệu tối ưu cho dự án của bạn.</p>
        </div>
    </a>
    """, unsafe_allow_html=True)

with cols[2]:
    st.markdown("""
    <a href="Thông tin kết nối" target="_self" class="card-link">
        <div class="feature-card">
            <div class="icon">🌐</div>
            <h3>Kết nối & Hỗ trợ</h3>
            <p>Tìm kiếm nhà phân phối trên bản đồ, khám phá thư viện tri thức và nhận tư vấn trực tiếp từ chatbot.</p>
        </div>
    </a>
    """, unsafe_allow_html=True)

st.divider()

# --- VỀ VIGLACERA ---
st.subheader("Về Viglacera và Cam kết Xanh")
st.write(
    """
    **Tổng công ty Viglacera - CTCP** tự hào là doanh nghiệp tiên phong trong lĩnh vực sản xuất VLXD xanh tại Việt Nam.
    Với kinh nghiệm và hệ thống nhà máy hiện đại, chúng tôi không ngừng nghiên cứu và phát triển
    các sản phẩm chất lượng cao, giảm thiểu tác động đến môi trường, góp phần xây dựng một tương lai bền vững.
    """
)
st.page_link("pages/4_Tương tác hỗ trợ.py", label="Tìm hiểu thêm và Liên hệ với chúng tôi", icon="➡️")

