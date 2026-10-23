from app.services.retriever import get_retriever


retriever = get_retriever("student1")


docs = retriever.invoke(
    "Explain CNN"
)


print("Total docs:",len(docs))


for d in docs:

    print("===================")
    print(d.page_content[:300])