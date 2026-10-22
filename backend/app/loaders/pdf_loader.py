from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pypdf import PdfReader

import os



def load_pdf(path):

    print("Loading PDF...")


    reader = PdfReader(path)


    documents=[]


    for index,page in enumerate(reader.pages):

        text = page.extract_text()


        if text and text.strip():

            documents.append(

                Document(
                    page_content=text,
                    metadata={
                        "page":index+1,
                        "source":os.path.basename(path)
                    }
                )

            )


    print(
        "Pages extracted:",
        len(documents)
    )


    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,
        chunk_overlap=200

    )


    chunks = splitter.split_documents(
        documents
    )


    print(
        "Chunks:",
        len(chunks)
    )


    return chunks