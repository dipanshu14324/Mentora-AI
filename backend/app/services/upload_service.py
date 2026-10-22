import os

from langchain_community.vectorstores import FAISS

from app.loaders.pdf_loader import load_pdf
from app.services.vector_store import get_embeddings



BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)


VECTOR_PATH = os.path.join(
    BASE_DIR,
    "vectordb"
)



def create_vector_database(
    pdf_path,
    user_id
):


    print("Loading PDF...")


    chunks = load_pdf(
        pdf_path
    )


    print(
        "Total chunks:",
        len(chunks)
    )


    if len(chunks) == 0:

        raise Exception(
            "No text extracted from PDF"
        )



    print(
        "Creating embeddings..."
    )


    db = FAISS.from_documents(

        chunks,

        get_embeddings()

    )



    user_path = os.path.join(

        VECTOR_PATH,

        str(user_id)

    )


    os.makedirs(

        user_path,

        exist_ok=True

    )


    db.save_local(

        user_path

    )


    print(
        "Vector database saved:"
    )


    print(
        user_path
    )


    return True