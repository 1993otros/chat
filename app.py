from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# CORS DEFINITIVO

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

# Modelo mensaje

class Message(BaseModel):
    message: str

# Ruta raíz

@app.get("/")
async def root():
    return {"status": "EMPRETUR IA funcionando"}

# Chat endpoint

@app.post("/chat")
async def chat(data: Message):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
                Eres EMPRETUR IA.
                Un asistente institucional de proyectos turísticos.
                Responde claro y profesionalmente.
                """
            },
            {
                "role": "user",
                "content": data.message
            }
        ]
    )

    return {
        "reply": response.choices[0].message.content
    }
