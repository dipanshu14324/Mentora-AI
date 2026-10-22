from fastapi import APIRouter

from app.services.chat_manager import get_chats


router = APIRouter(
    prefix="/history",
    tags=["Chat History"]
)


@router.get("/{user_id}")
def chat_history(user_id: str):

    chats = get_chats(user_id)

    return {
        "user_id": user_id,
        "chats": chats
    }