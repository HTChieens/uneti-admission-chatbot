import re
import unicodedata

from .retriever import retrieve
from .llm import generate_answer

FALLBACK_ANSWER = "Xin lỗi, tôi chưa có thông tin về nội dung này trong dữ liệu tuyển sinh hiện tại."
GREETING_ANSWER = "Chào bạn! Mình có thể hỗ trợ bạn các câu hỏi về tuyển sinh của trường."


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text.lower())
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def clean_pdf_text(text: str) -> str:
    return text.replace("trê n", "trên")


def is_greeting(question: str) -> bool:
    normalized_question = normalize_text(question).strip()
    return normalized_question in {"hi", "hello", "chao", "xin chao", "chao ban"}


def is_major_list_question(question: str) -> bool:
    normalized_question = normalize_text(question)
    return "nganh" in normalized_question and any(
        keyword in normalized_question
        for keyword in ("truong", "tuyen", "dao tao", "co nhung")
    )


def is_transcript_application_question(question: str) -> bool:
    normalized_question = normalize_text(question)
    return "hoc ba" in normalized_question and any(
        keyword in normalized_question
        for keyword in ("ho so", "giay to", "can gi", "dang ky", "xet")
    )


def get_all_documents(vectorstore):
    docstore = getattr(vectorstore, "docstore", None)
    documents = getattr(docstore, "_dict", {})
    return list(documents.values())


def extract_majors(vectorstore):
    majors = []
    seen_codes = set()
    pattern = re.compile(r"Mã ngành:\s*(\d+)\s*\|\s*Tên ngành:\s*([^\n\r]+)")

    for doc in get_all_documents(vectorstore):
        for code, name in pattern.findall(doc.page_content):
            if code in seen_codes:
                continue
            seen_codes.add(code)
            majors.append((code, name.strip()))

    return majors


def format_major_answer(majors):
    if not majors:
        return FALLBACK_ANSWER

    lines = ["Trường đang tuyển các ngành sau:"]
    lines.extend(f"- {name} ({code})" for code, name in majors)
    return "\n".join(lines)


def extract_transcript_application_documents(vectorstore):
    section_pattern = re.compile(
        r"2\.3\.3\.\s*Hồ sơ đăng ký xét tuyển:\s*(.*?)(?=2\.3\.4\.)",
        re.DOTALL
    )

    for doc in get_all_documents(vectorstore):
        match = section_pattern.search(doc.page_content)
        if not match:
            continue

        items = [
            clean_pdf_text(re.sub(r"\s+", " ", item)).strip(" -;")
            for item in re.split(r"\n\s*-\s*", match.group(1))
            if item.strip()
        ]
        return [item for item in items if item]

    return []


def format_transcript_application_answer(items):
    if not items:
        return FALLBACK_ANSWER

    lines = ["Hồ sơ xét học bạ gồm:"]
    lines.extend(f"- {item}" for item in items)
    return "\n".join(lines)


def ask(question, vectorstore):
    if is_greeting(question):
        return GREETING_ANSWER

    if is_major_list_question(question):
        return format_major_answer(extract_majors(vectorstore))

    if is_transcript_application_question(question):
        return format_transcript_application_answer(
            extract_transcript_application_documents(vectorstore)
        )

    docs = retrieve(vectorstore, question)
    if not docs:
        return FALLBACK_ANSWER

    answer = generate_answer(question, docs)
    return answer.content
