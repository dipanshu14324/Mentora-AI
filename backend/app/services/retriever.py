from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

import os



# =====================================
# Paths
# =====================================

USER_VECTOR_PATH = "app/vectordb"

DEFAULT_VECTOR_PATH = "app/vector_db"




# =====================================
# Load Retriever
# =====================================

def get_retriever(user_id=None):

    try:


        embeddings = HuggingFaceEmbeddings(

            model="sentence-transformers/all-MiniLM-L6-v2"

        )


        vector_path = None



        # -----------------------------
        # User PDF Vector Database
        # -----------------------------

        if user_id:


            user_path = os.path.join(

                USER_VECTOR_PATH,

                str(user_id)

            )


            print(
                "Checking user vector:",
                user_path
            )


            if os.path.isdir(user_path):


                faiss_file = os.path.join(user_path, "index.faiss")
                pkl_file = os.path.join(user_path, "index.pkl")

                if os.path.exists(faiss_file) and os.path.exists(pkl_file):
                    vector_path = user_path



        # -----------------------------
        # Select Database
        # -----------------------------


        if vector_path:


            print(
                "Loading USER PDF Vector DB:",
                vector_path
            )


        else:


            vector_path = DEFAULT_VECTOR_PATH


            print(
                "Loading DEFAULT Vector DB:",
                vector_path
            )



        # -----------------------------
        # Load FAISS
        # -----------------------------


        db = FAISS.load_local(

            vector_path,

            embeddings,

            allow_dangerous_deserialization=True

        )


        print("=" * 60)
        print("FAISS Loaded Successfully")
        print("Vector Path :", vector_path)
        print("Documents :", db.index.ntotal)
        print("=" * 60)



        retriever = db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={

                "k":3,

                "score_threshold":0.5

            }

        )


        return retriever



    except Exception as e:


        import traceback

        print("=" * 60)
        print("Retriever Loading Error")
        traceback.print_exc()
        print("=" * 60)


        return None