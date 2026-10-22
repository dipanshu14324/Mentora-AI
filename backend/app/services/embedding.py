from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import os
import traceback


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)


VECTOR_PATH = os.path.join(
    BASE_DIR,
    "vectordb"
)



def create_vector_store(
    documents,
    user_id
):

    try:

        print("="*60)
        print("Creating Vector Database")
        print("Documents:", len(documents))
        print("="*60)



        cleaned_documents = []

        seen=set()


        for doc in documents:

            text = doc.page_content.strip()


            if len(text)<30:
                continue


            if text in seen:
                continue


            seen.add(text)

            cleaned_documents.append(doc)



        if not cleaned_documents:

            return None



        print(
            "Loading embedding model..."
        )


        embeddings = HuggingFaceEmbeddings(

            model_name=
            "sentence-transformers/all-MiniLM-L6-v2"

        )


        print(
            "Embedding loaded"
        )



        vector_store = FAISS.from_documents(

            cleaned_documents,

            embeddings

        )



        save_path = os.path.join(

            VECTOR_PATH,

            str(user_id)

        )


        os.makedirs(
            save_path,
            exist_ok=True
        )



        vector_store.save_local(
            save_path
        )


        print(
            "FAISS saved:",
            save_path
        )


        return vector_store



    except Exception:

        traceback.print_exc()

        return None