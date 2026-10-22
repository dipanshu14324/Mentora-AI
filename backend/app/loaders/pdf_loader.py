from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pdf2image import convert_from_path

import pytesseract
import os
import cv2
import numpy as np



# ==========================
# Paths
# ==========================

POPPLER_PATH = r"C:\Users\DIPANSHU SHUKLA\Downloads\poppler\poppler-26.09.0\Library\bin"


TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH




# ==========================
# PDF Loader
# ==========================

def load_pdf(path):


    print("OCR Loading PDF...")



    pages = convert_from_path(

        path,

        dpi=300,

        poppler_path=POPPLER_PATH

    )



    print(
        "Total pages:",
        len(pages)
    )



    documents = []



    for index, page in enumerate(pages):


        print(
            f"OCR Page {index+1}/{len(pages)}"
        )



        try:


            # ==========================
            # Image Preprocessing
            # ==========================

            img = np.array(page)



            # RGB -> Gray

            gray = cv2.cvtColor(

                img,

                cv2.COLOR_RGB2GRAY

            )



            # Remove noise + improve contrast

            processed = cv2.threshold(

                gray,

                0,

                255,

                cv2.THRESH_BINARY + cv2.THRESH_OTSU

            )[1]



            # ==========================
            # OCR
            # ==========================

            text = pytesseract.image_to_string(

                processed,

                config="--psm 11"

            )



            if text.strip():

                documents.append(

                    Document(

                        page_content=text,

                        metadata={

                            "page": index + 1,

                            "source": os.path.basename(path)

                        }

                    )

                )



        except Exception as e:


            print(

                f"OCR Error Page {index+1}:",

                e

            )




    print(
        "Text pages:",
        len(documents)
    )



    # ==========================
    # Text Chunking
    # ==========================

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200

    )



    chunks = splitter.split_documents(

        documents

    )



    print(

        "Chunks created:",

        len(chunks)

    )



    return chunks