import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)


VECTOR_PATH = os.path.join(
    BASE_DIR,
    "vectordb"
)


def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def get_vector_store(user_id):

    user_path = os.path.join(
        VECTOR_PATH,
        str(user_id)
    )


    print("Looking vector path:")
    print(user_path)


    if not os.path.exists(user_path):

        print("No existing vector database found")
        return None


    try:

        db = FAISS.load_local(
            user_path,
            get_embeddings(),
            allow_dangerous_deserialization=True
        )

        print("Vector database loaded")

        return db


    except Exception as e:

        print(
            "Vector loading error:",
            e
        )

        return None


    try:

        db = FAISS.load_local(

            user_path,

            get_embeddings(),

            allow_dangerous_deserialization=True

        )


        print("Vector database loaded")

        return db


    except Exception as e:

        print(
            "Vector loading error:",
            e
        )

        return None