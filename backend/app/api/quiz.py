from fastapi import APIRouter
from pydantic import BaseModel

from app.services.quiz import QuizGenerator


router = APIRouter()


class QuizRequest(BaseModel):

    answer:str



@router.post("/quiz")
def generate_quiz(
    data:QuizRequest
):

    generator = QuizGenerator()


    questions = generator.generate(
        data.answer
    )


    return {

        "questions":questions

    }