from dotenv import load_dotenv
import os

load_dotenv()

print("GROQ KEY FOUND:",
      os.getenv("GROQ_API_KEY") is not None)
      
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.voice import router as voice_router
from app.api.chat import router as chat_router
from app.api.upload import router as upload_router
from app.api.material import router as material_router
from app.api.chat_history import router as history_router
from app.api.tts import router as tts_router
from app.api.flashcard import router as flashcard_router
from app.api.quiz import router as quiz_router
app = FastAPI(

    title="Mentora AI Tutor",

    version="1.0"

)


app.include_router(history_router)

# -------------------------
# CORS
# -------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)



# -------------------------
# API Routes
# -------------------------

app.include_router(
    chat_router
)

app.include_router(
    tts_router
)

app.include_router(
    flashcard_router
)

app.include_router(
    quiz_router
)

app.include_router(
    voice_router
)


app.include_router(
    upload_router
)


app.include_router(
    material_router
)



@app.get("/")
def home():

    return {

        "message":
        "Mentora Backend Running"

    }