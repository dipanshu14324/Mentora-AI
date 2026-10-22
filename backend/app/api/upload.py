from fastapi import APIRouter, UploadFile, File, Form

import os
import shutil
import uuid
import traceback


from app.loaders.pdf_loader import load_pdf
from app.services.embedding import create_vector_store


router = APIRouter()



# =====================================
# Paths
# =====================================

UPLOAD_PATH = "app/uploads"

VECTOR_PATH = "app/vectordb"



os.makedirs(
    UPLOAD_PATH,
    exist_ok=True
)



os.makedirs(
    VECTOR_PATH,
    exist_ok=True
)





# =====================================
# Upload PDF
# =====================================


@router.post("/upload")
async def upload_pdf(

    user_id: str = Form(...),

    file: UploadFile = File(...)

):


    file_path = None


    try:


        if not user_id:


            return {

                "status":"failed",

                "message":"User ID required"

            }



        if not file.filename.endswith(".pdf"):


            return {

                "status":"failed",

                "message":"Only PDF files allowed"

            }



        print("="*60)

        print("PDF Upload Started")

        print("User:", user_id)

        print("File:", file.filename)

        print("="*60)




        # =====================================
        # Remove old vector database
        # =====================================


        user_vector_path = os.path.join(

            VECTOR_PATH,

            user_id

        )


        if os.path.exists(user_vector_path):


            print(
                "Removing old vector DB..."
            )


            shutil.rmtree(
                user_vector_path
            )



        # =====================================
        # Save PDF temporarily
        # =====================================


        filename = (

            str(uuid.uuid4())

            +

            "_"

            +

            file.filename

        )



        file_path = os.path.join(

            UPLOAD_PATH,

            filename

        )



        with open(

            file_path,

            "wb"

        ) as buffer:


            shutil.copyfileobj(

                file.file,

                buffer

            )



        print(
            "PDF Saved:",
            file_path
        )




        # =====================================
        # Extract PDF Text
        # =====================================


        documents = load_pdf(

            file_path

        )



        print(
            "Extracted Chunks:",
            len(documents)
        )



        if not documents:


            return {


                "status":"failed",

                "message":
                "PDF contains no readable text"

            }




        # =====================================
        # Create FAISS Vector Store
        # =====================================


        vector_store = create_vector_store(

            documents,

            user_id

        )



        if vector_store is None:


            return {


                "status":"failed",

                "message":
                "Vector creation failed"

            }




        print("="*60)

        print("VECTOR DATABASE CREATED")

        print(
            "Location:",
            user_vector_path
        )

        print("="*60)




        return {


            "status":"success",

            "message":
            "PDF uploaded successfully",

            "user_id":
            user_id,

            "chunks":
            len(documents)

        }




    except Exception as e:


        print("="*60)

        print("UPLOAD ERROR")

        traceback.print_exc()

        print("="*60)



        return {


            "status":"error",

            "message":
            str(e)

        }




    finally:


        # =====================================
        # Remove temporary PDF
        # =====================================


        if file_path and os.path.exists(file_path):


            os.remove(
                file_path
            )


            print(
                "Temporary PDF removed"
            )