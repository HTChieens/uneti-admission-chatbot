def retrieve(vectorstore, query: str):
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5,}
    )
    docs = retriever.invoke(query)
    return list(docs)
