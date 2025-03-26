import streamlit as st
import requests

# Sidebar để nhập API URL
with st.sidebar:
    api_url = st.text_input("API URL", key="chatbot_api_url", value="http://localhost:8001/ask/")

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by your API")

# Khởi tạo session lưu tin nhắn
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Tôi có thể giúp gì cho bạn ?"}]

# Hiển thị tin nhắn trước đó
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Gửi tin nhắn mới
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Gọi API đúng định dạng
    try:
        with requests.post(api_url, json={"text": prompt}, stream=True) as response:
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            msg = ""  # Biến lưu nội dung chatbot gửi về
            chat_placeholder = st.empty()  # Tạo khung chat
            
            # Đọc từng phần dữ liệu từ stream
            for chunk in response.iter_content(chunk_size=32):
                if chunk:
                    text = chunk.decode("utf-8")
                    msg += text  # Ghép nội dung
                    chat_placeholder.markdown(msg)  # Cập nhật UI theo thời gian thực

            # Lưu tin nhắn chatbot vào session
            st.session_state.messages.append({"role": "assistant", "content": msg})
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling API: {e}")