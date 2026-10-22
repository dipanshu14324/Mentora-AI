from fastapi import APIRouter
from fastapi.responses import FileResponse
import edge_tts
import uuid
import os


router = APIRouter()


VOICE = "en-IN-NeerjaNeural"



@router.post("/text-to-speech")
async def text_to_speech(data: dict):


    text = data.get("text")


    if not text:

        return {
            "error":"Text missing"
        }



    filename = f"{uuid.uuid4()}.mp3"


    path = os.path.join(
        "audio",
        filename
    )


    os.makedirs(
        "audio",
        exist_ok=True
    )


    communicate = edge_tts.Communicate(
        text,
        VOICE
    )


    await communicate.save(path)



    return FileResponse(
        path,
        media_type="audio/mpeg"
    )