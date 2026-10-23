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
    save_message,
    generate_title
)


from app.services.flashcard import FlashcardGenerator
from app.services.quiz_generator import QuizGenerator



router = APIRouter()



flashcard_generator = FlashcardGenerator()

quiz_generator = QuizGenerator()





# =====================================================
# Request Models
# =====================================================


class ChatRequest(BaseModel):

    user_id: str

    session_id: str

    question: str

    level: str = "Beginner"

    style: str = "Concept Learning"




class RenameRequest(BaseModel):

    title: str






# =====================================================
# Create New Chat
# =====================================================


@router.post("/new-chat")
def new_chat(user_id:str):

    print("\n====================")
    print("NEW CHAT ROUTE")
    print("USER:", user_id)


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


    print("SESSION CREATED:", session_id)


    create_chat(
        user_id,
        session_id,
        None
    )


    print("CREATE_CHAT FINISHED")


    return {
        "message":"New chat created",
        "session_id":session_id
    }









# =====================================================
# Normal Chat
# =====================================================


@router.post("/chat")
def chat(data: ChatRequest):


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

            generate_title(data.question)

        )



        return {


            "answer":
            answer

        }



    except Exception as e:


        print(
            "CHAT ERROR:",
            e
        )


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )









# =====================================================
# Streaming Chat
# =====================================================


@router.post("/chat/stream")
def chat_stream(data: ChatRequest):


    print("STREAM STARTED")
    print("SESSION:", data.session_id)
    print("QUESTION:", data.question)



    tutor = MentoraTutor(

        session_id=data.session_id,
        user_id=data.user_id,
        level=data.level,
        style=data.style

    )



    def generate():

        try:

            full_answer = ""


            for chunk in tutor.stream_answer(
                data.question
            ):

                full_answer += chunk

                yield chunk



            # Save chat title after first question

            rename_chat(
                data.session_id,
                generate_title(data.question)
            )


            print(
                "CHAT TITLE UPDATED:",
                generate_title(data.question)
            )


            print(
                "STREAM FINISHED"
            )



        except Exception as e:


            print(
                "STREAM ERROR:",
                e
            )


            yield """
            I am temporarily unable to generate the explanation.
            Please try again.
            """



    return StreamingResponse(
    generate(),
    media_type="text/event-stream"
)




    











# =====================================================
# Chat History
# =====================================================


@router.get("/history/{user_id}")
def history(user_id:str):

    try:

        chats = get_chats(user_id)

        print("HISTORY:", chats)

        return {
            "user_id": user_id,
            "chats": chats
        }


    except Exception as e:

        print("HISTORY ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )









# =====================================================
# Get Messages
# =====================================================


@router.get("/messages/{session_id}")
def messages(session_id:str):


    return {


        "session_id":

        session_id,


        "messages":

        get_messages(session_id)

    }









# =====================================================
# Delete Chat
# =====================================================


@router.delete("/delete/{session_id}")
def remove_chat(session_id:str):


    try:


        delete_chat(session_id)


        return {


            "message":
            "Chat deleted"


        }



    except Exception as e:


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )









# =====================================================
# Rename Chat
# =====================================================


@router.put("/rename/{session_id}")
def rename(
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









# =====================================================
# Flashcards
# =====================================================


@router.post("/flashcards")
def create_flashcards(data:dict):


    answer = data["answer"]



    cards = flashcard_generator.generate(

        answer

    )


    return {


        "cards":

        cards

    }









# =====================================================
# Quiz
# =====================================================


@router.post("/quiz")
def generate_quiz(data:dict):


    text = data["answer"]



    questions = quiz_generator.generate(

        text

    )


    return {


        "questions":

        questions

    }

    @router.post("/chat")
    async def chat(request: ChatRequest):
    
        print("====================")
        print("CHAT REQUEST")
        print(request)
        print("====================")
    
        try:
        
            tutor = MentoraTutor(
                request.session_id
            )
    
    
            answer = tutor.answer(
                request.question
            )
    
    
            print("ANSWER GENERATED")
            print(answer)
    
    
            return {
                "answer":answer
            }
    
    
        except Exception as e:
        
            print("====================")
            print("CHAT ERROR")
            print(e)
            import traceback
            traceback.print_exc()
            print("====================")
    
    
            return {
                "error":str(e)
            }