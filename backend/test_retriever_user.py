from app.services.retriever import get_retriever


retriever = get_retriever("student1")


docs = retriever.invoke(
    "Explain RNN"
)


print("Documents:",len(docs))


for i,doc in enumerate(docs):

    print("\n----------------")
    print("DOC",i+1)
    print(doc.page_content[:500])