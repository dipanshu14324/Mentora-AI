from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

import os



BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)


VECTOR_PATH = os.path.join(
    BASE_DIR,
    "vector_db"
)




def process_pdf(file_path):


    print("Loading PDF...")


    loader = PyPDFLoader(
        file_path
    )


    documents = loader.load()



    print(
        "Pages:",
        len(documents)
    )



    splitter = RecursiveCharacterTextSplitter(

        chunk_size=300,

        chunk_overlap=50

    )



    chunks = splitter.split_documents(
        documents
    )



    print(
        "Chunks:",
        len(chunks)
    )



    embeddings = HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"

    )



    if os.path.exists(VECTOR_PATH):


        db = FAISS.load_local(

            VECTOR_PATH,

            embeddings,

            allow_dangerous_deserialization=True

        )


        db.add_documents(
            chunks
        )


    else:


        db = FAISS.from_documents(

            chunks,

            embeddings

        )



    db.save_local(
        VECTOR_PATH
    )



    return {

        "pages":
        len(documents),


        "chunks":
        len(chunks)

    }