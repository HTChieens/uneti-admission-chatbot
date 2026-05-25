from langchain_text_splitters import RecursiveCharacterTextSplitter
REGULATION_SEPARATORS = [
    r"\n(?=[IVX]+\.\s+[A-ZÀ-Ỹ])",          # Mức 1: I. THÔNG TIN CHUNG, II. TUYỂN SINH...
    r"\n(?=\d+\.\s+[A-ZÀ-Ỹa-zà-ỹ])",       # Mức 2: 1. Đối tượng..., 2. Mô tả...
    r"\n(?=\d+\.\d+\.\s+[A-ZÀ-Ỹa-zà-ỹ])",  # Mức 3: 2.1. Phương thức 1..., 2.2. Phương thức 2...
    r"\n(?=\d+\.\d+\.\d+\.\s+)",           # Mức 4: 2.2.1. Đối tượng..., 2.2.2. Xác định...
    r"\n(?=[a-z]\.\s+[A-ZÀ-Ỹa-zà-ỹ])",     # Mức 5: a., b., c.
    r"\n\n",                               # Phân tách đoạn văn
    r"\n",                                 # Phân tách dòng
    r"\.\s",                               # Phân tách câu (kết thúc bằng dấu chấm và khoảng trắng)
    r" "                                   # Phân tách từ (fallback cuối cùng)
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,      
    chunk_overlap=200,     
    add_start_index=True,
    strip_whitespace=True,
    separators=REGULATION_SEPARATORS,
    is_separator_regex= True
)

def split(docs):
    return splitter.split_documents(docs)

