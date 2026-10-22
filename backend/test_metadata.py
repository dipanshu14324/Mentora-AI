from app.services.retriever import get_retriever


retriever = get_retriever("student1")


docs = retriever.invoke(
    "Explain phishing attack"
)


for d in docs:

    print("----------------")
    print(d.metadata)
    print(d.page_content[:200])