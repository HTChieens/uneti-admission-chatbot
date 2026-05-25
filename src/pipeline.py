from .retriever import retrieve
from .llm import generate_answer
from pprint import pprint
from langchain_core.output_parsers import StrOutputParser
def ask(question, vectorstore):
    docs = retrieve(vectorstore, question)
    if not docs:
        return "Xin lỗi, tôi chưa có thông tin về nội dung này trong dữ liệu tuyển sinh hiện tại."

    answer = generate_answer(question, docs)

    return answer.content