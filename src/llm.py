from langchain_openai import ChatOpenAI

from .config import CHAT_MODEL
from .prompt import get_prompt_template


llm = ChatOpenAI(
    model=CHAT_MODEL,
    temperature=0,
)
prompt_template = get_prompt_template()
rag_chain = prompt_template | llm


def generate_answer(question, context_documents):
    cleaned_context = "\n\n".join(doc.page_content for doc in context_documents)
    response = rag_chain.invoke({
        "context": cleaned_context,
        "question": question
    })
    return response
