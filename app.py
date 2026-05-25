from src.vectorstore import load_vectorstore
from src.pipeline import ask
from pprint import pprint

db = load_vectorstore()
# while True:
#     ques = input("Nhập câu hỏi: ")
#     response = ask(ques, db)
#     print(response)
import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="UNETI TUYỂN SINH",
    page_icon="💬",
    layout="centered"
)

# =========================
# CSS TỐI GIẢN KIỂU CHATGPT
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

    # =========================
    # GỌI CHATBOT CỦA BẠN
    # =========================

    # Ví dụ:
    # response = ask_rag(prompt)

    # Tạm thời demo
    response = ask(prompt,db)

    # =========================
    # HIỂN THỊ RESPONSE
    # =========================
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })