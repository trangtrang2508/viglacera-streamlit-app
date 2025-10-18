import streamlit as st
import time

# --- CSS TÙY CHỈNH CHO GIAO DIỆN ---
st.markdown("""
<style>
    /* Thẻ chứa thông tin liên hệ và form */
    .contact-container {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    /* Cải thiện giao diện nút bấm trong form */
    .contact-container .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #0A488F;
        color: #FFFFFF;
        border: none;
        padding: 10px 0;
        transition: background-color 0.3s ease;
    }
    .contact-container .stButton>button:hover {
        background-color: #00A99D;
    }
    /* Nút gợi ý của chatbot */
    .stButton>button.suggestion-button {
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.85rem;
        border: 1px solid #0A488F;
        background-color: #FFFFFF;
        color: #0A488F;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    .stButton>button.suggestion-button:hover {
        background-color: #F0F2F6;
        border-color: #00A99D;
        color: #00A99D;
    }
</style>
""", unsafe_allow_html=True)


# --- HÀM LOGIC CHO CHATBOT (KỊCH BẢN NÂNG CẤP) ---
def get_basic_response(user_input):
    """
    Phân tích input của người dùng và trả về một câu trả lời dựa trên kịch bản chi tiết.
    """
    normalized_input = user_input.lower()

    # Nhóm 1: Câu hỏi về sản phẩm cụ thể
    if "gạch aac" in normalized_input or "bê tông khí" in normalized_input:
        return "Gạch bê tông khí chưng áp (AAC) của Viglacera là sản phẩm trọng lượng nhẹ, giúp giảm tải trọng công trình. Nó còn có khả năng cách âm, cách nhiệt và chống cháy vượt trội. Bạn có muốn biết về ứng dụng của nó không?"
    if "kính tiết kiệm năng lượng" in normalized_input or "kính low-e" in normalized_input:
        return "Kính tiết kiệm năng lượng (Low-E) của Viglacera giúp ngăn chặn sự truyền nhiệt từ môi trường bên ngoài, giữ cho không gian bên trong mát mẻ vào mùa hè và ấm áp vào mùa đông, từ đó giúp tiết kiệm đáng kể chi phí điện cho điều hòa."
    if "gạch ốp lát" in normalized_input or "gạch granite" in normalized_input:
        return "Viglacera có rất nhiều dòng gạch ốp lát với mẫu mã đa dạng. Các sản phẩm đều được sản xuất trên dây chuyền công nghệ xanh, đảm bảo độ bền và an toàn cho sức khỏe. Bạn có thể khám phá tất cả mẫu mã trong 'Thư viện Sản phẩm'."

    # Nhóm 2: Câu hỏi về đặc tính kỹ thuật & "xanh"
    elif "hệ số phát thải" in normalized_input or "dấu chân carbon" in normalized_input:
        return "Hệ số phát thải (Carbon Footprint) là chỉ số đo lường tổng lượng khí nhà kính phát thải trong suốt vòng đời sản phẩm. Sản phẩm có hệ số càng thấp thì càng thân thiện với môi trường. Bạn có thể dùng 'Công cụ Hỗ trợ' để ước tính chỉ số này cho từng sản phẩm."
    elif "bền vững" in normalized_input or "thân thiện môi trường" in normalized_input:
        return "Tính bền vững là cốt lõi trong các sản phẩm của Viglacera. Chúng tôi ưu tiên sử dụng vật liệu tái chế, quy trình sản xuất tiết kiệm năng lượng và giảm thiểu phát thải CO2. Các chứng nhận xanh là minh chứng rõ nhất cho cam kết này."
    elif "chứng nhận" in normalized_input or "chứng chỉ" in normalized_input:
        return "Các sản phẩm xanh của chúng tôi đạt nhiều chứng nhận uy tín như TCVN, QCVN, Nhãn Xanh Singapore, và kiểm định PCCC của Bộ Công An. Mỗi sản phẩm trong 'Thư viện Sản phẩm' đều có ghi rõ các chứng nhận đạt được."

    # Nhóm 3: Câu hỏi về thương mại và hỗ trợ
    elif "giá" in normalized_input or "báo giá" in normalized_input:
        return "Cảm ơn bạn đã quan tâm! Để nhận báo giá chính xác và tốt nhất, vui lòng liên hệ trực tiếp với các nhà phân phối chính hãng của chúng tôi. Bạn có thể tìm nhà phân phối gần nhất tại trang 'Thông tin & Kết nối'."
    elif "mua ở đâu" in normalized_input or "nhà phân phối" in normalized_input or "đại lý" in normalized_input:
        return "Bạn có thể tìm kiếm các đại lý và nhà phân phối của Viglacera trên toàn quốc tại trang 'Thông tin & Kết nối'. Trang đó có một bản đồ tương tác và danh sách chi tiết để bạn dễ dàng liên hệ!"
    elif "liên hệ" in normalized_input or "hỗ trợ" in normalized_input:
        return "Bạn có thể sử dụng form liên hệ ở ngay bên cạnh để gửi yêu cầu hỗ trợ trực tiếp cho chúng tôi. Đội ngũ Viglacera sẽ phản hồi bạn trong thời gian sớm nhất."

    # Nhóm 4: Lời chào và các câu hỏi chung
    elif "chào" in normalized_input or "hello" in normalized_input:
        return "Chào bạn! Tôi là chatbot tư vấn của Viglacera. Tôi có thể giúp gì cho bạn về các sản phẩm và giải pháp vật liệu xây dựng xanh?"
    else:
        # Câu trả lời mặc định
        return "Cảm ơn câu hỏi của bạn! Đây là một vấn đề chuyên sâu. Để được tư vấn tốt nhất, bạn vui lòng điền thông tin vào form liên hệ bên cạnh, chuyên viên của chúng tôi sẽ hỗ trợ bạn chi tiết hơn."

# --- HÀM XỬ LÝ GỬI TIN NHẮN ---
def send_message(message):
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user"):
        st.markdown(message)

    with st.chat_message("assistant"):
        with st.spinner("Đang nghĩ..."):
            time.sleep(1)
            response = get_basic_response(message)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- GIAO DIỆN CHÍNH ---
st.title("Tương tác và Hỗ trợ 💬")
st.write("Kết nối với chúng tôi qua chatbot hoặc gửi phản hồi trực tiếp.")

col1, col2 = st.columns([0.6, 0.4])

with col1:
    # --- HỆ THỐNG TƯ VẤN ẢO (AI CHATBOT) ---
    st.subheader("Chatbot tư vấn Viglacera")

    # Khởi tạo lịch sử tin nhắn
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Chào bạn! Tôi có thể giúp gì cho bạn về các sản phẩm vật liệu xây dựng xanh của Viglacera?"}]

    # Hiển thị các tin nhắn cũ
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input từ người dùng
    if prompt := st.chat_input("Bạn có câu hỏi gì?"):
        send_message(prompt)

    # Các nút gợi ý
    st.markdown("Gợi ý:")
    suggestions = ["Ưu điểm gạch AAC?", "Tìm nhà phân phối ở đâu?", "Sản phẩm có bền vững không?"]
    s_cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        if s_cols[i].button(suggestion, key=f"suggestion_{i}", use_container_width=True):
            # Sử dụng CSS class để tùy chỉnh nút
            st.markdown(f'<style>.stButton>button[key="suggestion_{i}"] {{ { " ".join( "suggestion-button".split()) } }}</style>', unsafe_allow_html=True)
            send_message(suggestion)

with col2:
    # --- TRANG GIỚI THIỆU & LIÊN HỆ ---
    st.markdown('<div class="contact-container">', unsafe_allow_html=True)
    st.subheader("Giới thiệu & Liên hệ")
    st.write(
        """
        **Tổng công ty Viglacera - CTCP** tự hào là đơn vị tiên phong trong lĩnh vực sản xuất VLXD xanh tại Việt Nam, cam kết về chất lượng, đổi mới và bền vững.
        
        Chúng tôi luôn sẵn lòng lắng nghe và hỗ trợ bạn.
        """
    )
    
    # Form liên hệ
    with st.form("contact_form", clear_on_submit=True):
        st.write("##### Gửi phản hồi cho chúng tôi")
        name = st.text_input("Tên của bạn:", placeholder="Nguyễn Văn A")
        email = st.text_input("Email của bạn:", placeholder="example@email.com")
        message = st.text_area("Nội dung tin nhắn:", placeholder="Tôi cần tư vấn về sản phẩm...")
        submitted = st.form_submit_button("Gửi phản hồi")

        if submitted:
            if name and email and message:
                st.success("Cảm ơn bạn, phản hồi của bạn đã được gửi thành công!")
            else:
                st.error("Vui lòng điền đầy đủ tất cả các trường.")
    st.markdown('</div>', unsafe_allow_html=True)

