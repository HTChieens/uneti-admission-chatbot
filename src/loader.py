from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from pprint import pprint
loader = DirectoryLoader(
    path="./data/documents",
    glob = "**/*.pdf",
    loader_cls= PyPDFLoader,
    show_progress= True,
    use_multithreading= True
)
def load_pdf():
    return loader.load()
import re
from langchain_core.documents import Document

def clean_and_merge_docs(docs):
    full_text = ""
    
    for doc in docs:
        text = doc.page_content
        
        # 1. Xóa Header / Footer thừa của trường (nếu chúng xuất hiện lặp lại)
        # Bạn có thể điều chỉnh regex này cho khớp chính xác với chuỗi rác
        text = re.sub(r"BỘ CÔNG THƯƠNG\s+TRƯỜNG ĐẠI HỌC\s+KINH TẾ - KỸ THUẬT CÔNG NGHIỆP.*?", "", text, flags=re.DOTALL)
        text = re.sub(r"CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\s+Độc lập - Tự do - Hạnh phúc", "", text)
        
        # 2. Xóa số trang ở đầu dòng hoặc cuối dòng (ví dụ: "2 \n \n" hoặc "\n 4")
        text = re.sub(r"^\s*\d+\s*\n", "", text) 
        text = re.sub(r"\n\s*\d+\s*$", "", text)
        
        # Nối text của trang này vào chuỗi tổng thể, đảm bảo có dấu xuống dòng
        full_text += text.strip() + "\n"
    
    # Tạo lại MỘT Document duy nhất chứa toàn bộ văn bản liên mạch
    # (Chấp nhận đánh đổi là metadata 'page' sẽ tính là một nguồn tổng thể, 
    # nhưng đổi lại chunk sẽ không bao giờ bị gãy đôi câu giữa 2 trang)
    cleaned_document = Document(
        page_content=full_text,
        metadata={"source": docs[0].metadata.get("source", "unknown")}
    )
    
    return [cleaned_document]