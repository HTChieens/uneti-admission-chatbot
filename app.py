from src.vectorstore import load_vectorstore
from src.pipeline import ask
from pprint import pprint

db = load_vectorstore()
while True:
    ques = input("Nhập câu hỏi: ")
    response = ask(ques, db)
    print(response)