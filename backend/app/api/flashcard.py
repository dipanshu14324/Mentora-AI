from fastapi import APIRouter
from pydantic import BaseModel

from app.services.flashcard import FlashcardGenerator


router = APIRouter()


generator = FlashcardGenerator()



class FlashcardRequest(BaseModel):

    answer: str



@router.post("/flashcards")
def generate_flashcards(
    request: FlashcardRequest
):

    cards = generator.generate(
        request.answer
    )


    return {
        "cards": cards
    }