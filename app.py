import streamlit as st

from src.pipeline import ask
from src.vectorstore import load_vectorstore


# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="UNETI TUYỂN SINH",
    page_icon="💬",
    layout="centered"
)

# =========================
# CSS TỐI GIẢN
# =========================
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        max-width: 850px;
    }

    .stChatMessage {
        border-radius: 12px;
        padding: 0.5rem;
    }

    header, footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Đang tải dữ liệu tuyển sinh...")
def get_vectorstore():
    return load_vectorstore()

# =========================
# TIÊU ĐỀ
# =========================
st.title("UNETI TUYỂN SINH")

# =========================
# LƯU LỊCH SỬ CHAT
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# HIỂN THỊ LỊCH SỬ CHAT
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# NHẬP CÂU HỎI
# =========================
prompt = st.chat_input("Nhập câu hỏi tuyển sinh...")

# =========================
# XỬ LÝ CHAT
# =========================
if prompt:
    # Hiển thị user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    response = ask(prompt, get_vectorstore())

    # =========================
    # HIỂN THỊ RESPONSE
    # =========================
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
