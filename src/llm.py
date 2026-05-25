import os
from .prompt import get_prompt_template 
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
llm = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)
prompt_template = get_prompt_template()
rag_chain = prompt_template | llm

def generate_answer(question, context_documents):
    cleaned_context = "\n\n".join([doc.page_content for doc in context_documents])
    response = rag_chain.invoke({
        "context": cleaned_context,
        "question": question
    })
    return response