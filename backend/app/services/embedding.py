from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

import os
import traceback



# =====================================
# Paths
# =====================================

VECTOR_PATH = os.path.join(
    "app",
    "vectordb"
)





# =====================================
# Create Vector Store
# =====================================


def create_vector_store(
    documents,
    user_id
):


    try:


        print("="*60)

        print("Creating Vector Database")

        print("Total Input Documents:",
              len(documents))

        print("="*60)



        # =====================================
        # Clean Documents
        # =====================================


        cleaned_documents = []


        seen = set()



        for doc in documents:


            text = doc.page_content.strip()



            # Remove empty chunks

            if len(text) < 30:

                continue



            # Remove duplicate chunks

            if text in seen:

                continue



            seen.add(text)



            cleaned_documents.append(doc)



        print(
            "After Cleaning:",
            len(cleaned_documents)
        )



        if len(cleaned_documents)==0:


            print(
                "No valid documents found"
            )


            return None





        # =====================================
        # Embedding Model
        # =====================================


        embeddings = OllamaEmbeddings(

            model="nomic-embed-text"

        )



        print(
            "Embedding model loaded"
        )





        # =====================================
        # Create FAISS
        # =====================================


        vector_store = FAISS.from_documents(

            cleaned_documents,

            embeddings

        )



        print(
            "FAISS index created"
        )





        # =====================================
        # User Vector Path
        # =====================================


        save_path = os.path.join(

            VECTOR_PATH,

            str(user_id)

        )



        os.makedirs(

            save_path,

            exist_ok=True

        )




        # =====================================
        # Save Vector DB
        # =====================================


        vector_store.save_local(

            save_path

        )



        print("="*60)

        print(
            "Vector Database Saved"
        )

        print(
            "Path:",
            save_path
        )

        print(
            "Vectors:",
            vector_store.index.ntotal
        )

        print("="*60)



        return vector_store





    except Exception as e:


        print("="*60)

        print(
            "Embedding Error"
        )


        traceback.print_exc()

        print("="*60)



        return None