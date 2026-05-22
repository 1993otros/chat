from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Modelo

class Message(BaseModel):
    message: str

# Root

@app.get("/")
async def root():

    return {
        "status": "ok"
    }

# Chat

@app.post("/chat")
async def chat(data: Message):

    pregunta = data.message

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
                Eres EMPRETUR IA.
                Asistente institucional.
                """
            },
            {
                "role": "user",
                "content": pregunta
            }
        ]
    )

    return {
        "reply": response.choices[0].message.content
    }
