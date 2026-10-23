from app.services.retriever import get_retriever


r = get_retriever("student1")


print(r.vectorstore.index.d)