from .config import RETRIEVER_FETCH_K, RETRIEVER_K


QUERY_EXPANSIONS = {
    "học bạ": "xét kết quả học tập THPT hồ sơ đăng ký xét tuyển phương thức xét tuyển học bạ",
    "hoc ba": "xét kết quả học tập THPT hồ sơ đăng ký xét tuyển phương thức xét tuyển học bạ",
    "ngành": "danh sách ngành mã ngành tên ngành chỉ tiêu tuyển sinh",
    "nganh": "danh sách ngành mã ngành tên ngành chỉ tiêu tuyển sinh",
    "tuyển ngành": "danh sách ngành đào tạo mã ngành tên ngành chỉ tiêu tuyển sinh",
    "tuyen nganh": "danh sách ngành đào tạo mã ngành tên ngành chỉ tiêu tuyển sinh",
}


def expand_query(query: str) -> str:
    normalized_query = query.lower()
    expansions = [
        expansion
        for keyword, expansion in QUERY_EXPANSIONS.items()
        if keyword in normalized_query
    ]
    if not expansions:
        return query

    return f"{query}\n{' '.join(expansions)}"


def retrieve(vectorstore, query: str):
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": RETRIEVER_K,
            "fetch_k": RETRIEVER_FETCH_K,
        }
    )
    docs = retriever.invoke(expand_query(query))
    return list(docs)
