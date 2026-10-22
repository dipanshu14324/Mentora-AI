from fastapi import APIRouter, UploadFile, File
from faster_whisper import WhisperModel
import tempfile
import os


router = APIRouter()


model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)



@router.post("/voice-to-text")
async def voice_to_text(
    file: UploadFile = File(...)
):

    audio_path = None

    try:

        with tempfile.NamedTemporaryFile(
            suffix=".webm",
            delete=False
        ) as temp:


            temp.write(
                await file.read()
            )


            audio_path = temp.name



        segments, info = model.transcribe(
            audio_path
        )


        text = ""


        for segment in segments:

            text += segment.text



        return {
            "text": text.strip()
        }



    finally:

        if audio_path and os.path.exists(audio_path):

            os.remove(audio_path)