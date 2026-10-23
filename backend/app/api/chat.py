from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uuid


from app.services.tutor import MentoraTutor

from app.services.chat_manager import (
    create_chat,
    get_chats,
    get_messages,
    delete_chat,
    rename_chat,
    generate_title
)


from app.services.flashcard import FlashcardGenerator
from app.services.quiz_generator import QuizGenerator



router = APIRouter()


flashcard_generator = FlashcardGenerator()

quiz_generator = QuizGenerator()



# =====================================
# Models
# =====================================

class ChatRequest(BaseModel):

    user_id: str

    session_id: str

    question: str

    level: str = "Beginner"

    style: str = "Concept Learning"



class RenameRequest(BaseModel):

    title: str





# =====================================
# New Chat
# =====================================

@router.post("/new-chat")
def new_chat(user_id:str):

    if not user_id:

        raise HTTPException(
            status_code=400,
            detail="User ID required"
        )


    session_id = (
        user_id
        +
        "_"
        +
        str(uuid.uuid4())[:8]
    )


    create_chat(
        user_id,
        session_id,
        None
    )


    return {

        "message":"New chat created",

        "session_id":session_id

    }






# =====================================
# Normal Chat
# =====================================

@router.post("/chat")
def chat(data: ChatRequest):


    print("====================")
    print("CHAT REQUEST")
    print(data)
    print("====================")


    try:


        tutor = MentoraTutor(

            session_id=data.session_id,

            user_id=data.user_id,

            level=data.level,

            style=data.style

        )


        answer = tutor.answer(
            data.question
        )


        rename_chat(

            data.session_id,

            generate_title(
                data.question
            )

        )


        print("ANSWER GENERATED")

        return {

            "answer":answer

        }



    except Exception as e:


        print("CHAT ERROR:")
        print(e)


        import traceback

        traceback.print_exc()


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )






# =====================================
# Streaming Chat
# =====================================


@router.post("/chat/stream")
def chat_stream(data:ChatRequest):


    print("STREAM REQUEST")

    print(data)



    tutor = MentoraTutor(

        session_id=data.session_id,

        user_id=data.user_id,

        level=data.level,

        style=data.style

    )



    def generate():


        try:


            for chunk in tutor.stream_answer(
                data.question
            ):


                yield chunk



            rename_chat(

                data.session_id,

                generate_title(
                    data.question
                )

            )



        except Exception as e:


            print(
                "STREAM ERROR:",
                e
            )


            yield "Unable to generate answer."



    return StreamingResponse(

        generate(),

        media_type="text/plain"

    )







# =====================================
# History
# =====================================

@router.get("/history/{user_id}")
def history(user_id:str):


    return {

        "user_id":user_id,

        "chats":get_chats(user_id)

    }






# =====================================
# Messages
# =====================================

@router.get("/messages/{session_id}")
def messages(session_id:str):


    return {

        "session_id":session_id,

        "messages":
        get_messages(session_id)

    }






# =====================================
# Delete Chat
# =====================================

@router.delete("/delete/{session_id}")
def remove_chat(session_id:str):


    delete_chat(session_id)


    return {

        "message":"Chat deleted"

    }







# =====================================
# Rename
# =====================================

@router.put("/rename/{session_id}")
def rename_chat_route(
    session_id:str,
    data:RenameRequest
):


    rename_chat(

        session_id,

        data.title

    )


    return {

        "message":"Renamed successfully"

    }







# =====================================
# Flashcards
# =====================================

@router.post("/flashcards")
def create_flashcards(data:dict):


    cards = flashcard_generator.generate(

        data["answer"]

    )


    return {

        "cards":cards

    }







# =====================================
# Quiz
# =====================================

@router.post("/quiz")
def generate_quiz(data:dict):


    questions = quiz_generator.generate(

        data["answer"]

    )


    return {

        "questions":questions

    }