# pages/4_Tuong_tac_Ho_tro.py
import streamlit as st
import time

st.title("Tương tác và Hỗ trợ 💬")
st.write("Kết nối với chúng tôi qua chatbot hoặc gửi phản hồi trực tiếp.")

# -------------------------------------------------------------------
## BƯỚC 1: TẠO HÀM LOGIC CHO CHATBOT
# -------------------------------------------------------------------
# Hàm này sẽ chứa logic để trả lời các câu hỏi dựa trên từ khóa.
# Bạn có thể dễ dàng thêm các câu trả lời mới ở đây.
def get_basic_response(user_input):
    """
    Phân tích input của người dùng và trả về một câu trả lời dựa trên từ khóa.
    """
    normalized_input = user_input.lower() # Chuyển thành chữ thường để dễ so sánh

    if "gạch" in normalized_input:
        return "Viglacera có nhiều dòng sản phẩm gạch xanh, nổi bật là gạch bê tông khí chưng áp (AAC). Sản phẩm này rất nhẹ, cách âm, cách nhiệt tốt và thân thiện với môi trường."

    elif "chứng nhận" in normalized_input or "chứng chỉ" in normalized_input:
        return "Các sản phẩm xanh của chúng tôi đạt nhiều chứng nhận uy tín như Chứng nhận TCVN, Nhãn Xanh của Singapore, và các kiểm định phòng cháy chữa cháy của Bộ Công An. Bạn có thể xem chi tiết trong Thư viện Sản phẩm."

    elif "giá" in normalized_input or "báo giá" in normalized_input:
        return "Cảm ơn bạn đã quan tâm! Về vấn đề báo giá chi tiết, vui lòng liên hệ trực tiếp với bộ phận kinh doanh hoặc các nhà phân phối chính hãng của chúng tôi. Bạn có thể tìm nhà phân phối gần nhất ở trang 'Thông tin & Kết nối'."

    elif "mua ở đâu" in normalized_input or "nhà phân phối" in normalized_input:
        return "Bạn có thể tìm kiếm các đại lý và nhà phân phối của Viglacera trên toàn quốc tại trang 'Thông tin & Kết nối'. Trang đó có một bản đồ tương tác rất tiện lợi!"
        
    elif "liên hệ" in normalized_input:
        return "Bạn có thể sử dụng form liên hệ ở ngay bên dưới để gửi phản hồi trực tiếp cho chúng tôi. Chúng tôi sẽ phản hồi trong thời gian sớm nhất."

    else:
        # Câu trả lời mặc định nếu không tìm thấy từ khóa
        return "Cảm ơn câu hỏi của bạn! Hiện tại tôi chỉ có thể trả lời một số câu hỏi cơ bản. Vui lòng liên hệ bộ phận hỗ trợ qua form bên dưới nếu bạn cần thông tin chi tiết hơn."

# --- Hệ thống tư vấn ảo (AI Chatbot) ---
st.subheader("Chatbot tư vấn Viglacera")

# Khởi tạo lịch sử tin nhắn
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Chào bạn! Tôi có thể giúp gì cho bạn về các sản phẩm vật liệu xây dựng xanh của Viglacera?"}]

# Hiển thị các tin nhắn cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Xử lý input mới
if prompt := st.chat_input("Bạn có câu hỏi gì?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang nghĩ..."):
            time.sleep(1)
            # -------------------------------------------------------------------
            ## BƯỚC 2: GỌI HÀM LOGIC Ở ĐÂY
            # -------------------------------------------------------------------
            response = get_basic_response(prompt)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown("---")

# --- Form liên hệ (Giữ nguyên không đổi) ---
st.subheader("Giới thiệu & Liên hệ")
st.write(
    """
    Viglacera tự hào là một trong những đơn vị hàng đầu trong lĩnh vực sản xuất
    vật liệu xây dựng tại Việt Nam...
    """
)
with st.form("contact_form", clear_on_submit=True):
    st.subheader("Gửi phản hồi cho chúng tôi")
    name = st.text_input("Tên của bạn:")
    email = st.text_input("Email của bạn:")
    message = st.text_area("Nội dung tin nhắn:")
    submitted = st.form_submit_button("Gửi phản hồi")
    if submitted:
        if name and email and message:
            st.success("Cảm ơn bạn, phản hồi của bạn đã được gửi thành công!")
        else:
            st.error("Vui lòng điền đầy đủ tất cả các trường.")