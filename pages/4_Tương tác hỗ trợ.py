import streamlit as st
import time
import requests # Thư viện để gọi API

# --- SIDEBAR (Để đồng bộ giao diện) ---
with st.sidebar:
    st.image("images/download.png", use_container_width=True)
    st.title("Về Viglacera Xanh")
    st.markdown("""
    **Cổng thông tin VLXD Xanh** là một sáng kiến của Viglacera nhằm cung cấp kiến thức và công cụ để hỗ trợ các dự án xây dựng bền vững tại Việt Nam.
    """)
    st.divider()
    st.markdown("🔗 **Liên kết hữu ích**")
    st.link_button("Trang chủ Viglacera 🏠", "https://viglacera.com.vn/", use_container_width=True)
    # QUAN TRỌNG: Đảm bảo tên file này khớp chính xác với file trong thư mục 'pages' của bạn.
    st.page_link("pages/4_Tương tác hỗ trợ.py", label="Liên hệ chúng tôi ✉️", use_container_width=True)

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
        height: 100%; /* Giúp 2 cột bằng nhau */
    }
    .contact-container .stButton>button { width: 100%; border-radius: 8px; background-color: #0A488F; color: #FFFFFF; border: none; padding: 10px 0; transition: background-color 0.3s ease; }
    .contact-container .stButton>button:hover { background-color: #00A99D; }
    
    /* Container cho các nút gợi ý */
    .suggestion-container .stButton>button {
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.85rem;
        border: 1px solid #0A488F;
        background-color: #FFFFFF;
        color: #0A488F;
        transition: all 0.3s ease;
        font-weight: 600;
        width: 100%;
    }
    .suggestion-container .stButton>button:hover {
        background-color: #F0F2F6;
        border-color: #00A99D;
        color: #00A99D;
    }
</style>
""", unsafe_allow_html=True)


# --- HÀM LOGIC MỚI CHO CHATBOT (SỬ DỤNG GEMINI API) ---
@st.cache_data(show_spinner=False)
def get_ai_response(user_input, chat_history):
    """
    Gửi yêu cầu đến Gemini API và nhận phản hồi từ AI, với khả năng xử lý lỗi chi tiết.
    """
    if "GEMINI_API_KEY" not in st.secrets:
        return "Lỗi cấu hình: Không tìm thấy `GEMINI_API_KEY`. Vui lòng tạo file `.streamlit/secrets.toml` và thêm key của bạn vào đó."
        
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        return "Lỗi cấu hình: Giá trị của `GEMINI_API_KEY` đang bị trống. Vui lòng kiểm tra lại file `.streamlit/secrets.toml`."

    # Sửa lại API URL cho chính xác
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"
    
    # Hoàn thiện kịch bản cho AI
    system_prompt = """
    Bạn là một trợ lý ảo am hiểu và chuyên nghiệp của Tổng công ty Viglacera. 
    Vai trò của bạn là tư vấn cho khách hàng về các sản phẩm vật liệu xây dựng (VLXD) xanh của Viglacera.
    - Tông giọng: Thân thiện, chuyên nghiệp, và hữu ích.
    - Kiến thức: Chỉ tập trung vào các sản phẩm của Viglacera như Gạch bê tông khí chưng áp (AAC), Kính tiết kiệm năng lượng (Low-E), Gạch ốp lát, thiết bị vệ sinh, v.v. và các khái niệm liên quan đến xây dựng xanh.
    - Quy tắc: 
      1. KHÔNG trả lời các câu hỏi không liên quan đến Viglacera hoặc VLXD. Nếu được hỏi, hãy lịch sự trả lời: "Tôi là trợ lý ảo của Viglacera và chỉ có thể cung cấp thông tin về các sản phẩm và giải pháp của chúng tôi."
      2. KHÔNG bịa đặt thông tin. Nếu không biết câu trả lời, hãy nói: "Đây là một câu hỏi rất hay. Để có câu trả lời chính xác nhất, bạn vui lòng điền thông tin vào form liên hệ bên cạnh, chuyên viên của chúng tôi sẽ hỗ trợ bạn."
      3. Giữ câu trả lời ngắn gọn, dễ hiểu.
      4. Khi được hỏi về "giá" hoặc "mua ở đâu", hãy hướng dẫn người dùng đến trang "Thông tin & Kết nối" hoặc liên hệ nhà phân phối.
    """
    
    history_for_api = []
    for message in chat_history:
        role = "user" if message["role"] == "user" else "model"
        history_for_api.append({"role": role, "parts": [{"text": message["content"]}]})

    payload = {
        "contents": [*history_for_api, {"role": "user", "parts": [{"text": user_input}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=20)
        response.raise_for_status() 
        result = response.json()
        
        if "error" in result:
             return f"Lỗi từ API: {result['error']['message']}"

        candidate = result.get("candidates", [{}])[0]
        if candidate.get("finishReason") == "SAFETY":
            return "Rất tiếc, câu hỏi của bạn đã vi phạm chính sách an toàn và không thể được trả lời."

        text_part = candidate.get("content", {}).get("parts", [{}])[0]
        return text_part.get("text", "Xin lỗi, tôi chưa thể trả lời câu hỏi này. Vui lòng thử lại sau.")

    except requests.exceptions.HTTPError as err:
        return f"Lỗi HTTP {err.response.status_code}: Yêu cầu đến server thất bại. Rất có thể **API Key của bạn không hợp lệ** hoặc đã hết hạn. Vui lòng kiểm tra lại."
    except requests.exceptions.RequestException:
        return "Lỗi kết nối mạng. Vui lòng kiểm tra lại kết nối Internet của bạn."
    except (KeyError, IndexError):
        return "Rất tiếc, tôi nhận được phản hồi không hợp lệ từ server. Vui lòng thử lại."

# --- GIAO DIỆN CHÍNH ---
st.title("Tương tác và Hỗ trợ 💬")
st.write("Kết nối với chúng tôi qua chatbot hoặc gửi phản hồi trực tiếp.")

col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.subheader("Chatbot tư vấn Viglacera")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Chào bạn! Tôi là trợ lý ảo của Viglacera. Tôi có thể giúp gì cho bạn?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Hợp nhất logic xử lý input
    user_input = None
    if prompt := st.chat_input("Bạn có câu hỏi gì?"):
        user_input = prompt

    st.write("Hoặc thử một trong các câu hỏi sau:")
    # Bọc các nút gợi ý trong container để áp dụng CSS
    with st.container():
        st.markdown('<div class="suggestion-container">', unsafe_allow_html=True)
        suggestions = ["Ưu điểm gạch AAC?", "Kính Low-E là gì?", "Tìm nhà phân phối ở đâu?"]
        s_cols = st.columns(len(suggestions))
        for i, suggestion in enumerate(suggestions):
            if s_cols[i].button(suggestion, key=f"suggestion_{i}"):
                user_input = suggestion
        st.markdown('</div>', unsafe_allow_html=True)

    # Xử lý input sau khi đã nhận
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Vui lòng chờ giây lát..."):
                response = get_ai_response(user_input, st.session_state.messages[:-1])
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col2:
    st.markdown('<div class="contact-container">', unsafe_allow_html=True)
    st.subheader("Giới thiệu & Liên hệ")
    st.write(
        """
        **Tổng công ty Viglacera - CTCP** tự hào là đơn vị tiên phong trong lĩnh vực sản xuất VLXD xanh tại Việt Nam, cam kết về chất lượng, đổi mới và bền vững.
        
        Chúng tôi luôn sẵn lòng lắng nghe và hỗ trợ bạn.
        """
    )
    
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

