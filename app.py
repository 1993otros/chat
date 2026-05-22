from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import pandas as pd
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
    api_key=os.getenv("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")
)

# GOOGLE SHEETS CSV

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQKY9V7t5EUEgVSFf-cY8R-LAPeg7XTgD5XIACALr4v0v7F7jI-7jhwpu0v8zIJ-ezfITqb0f4N8OFB/pub?gid=812671645&single=true&output=csv"

# Leer Google Sheet

df = pd.read_csv(SHEET_URL)

# Modelo mensaje

class Message(BaseModel):
    message: str

# Ruta raíz

@app.get("/")
async def root():
    return {"status": "EMPRETUR IA funcionando"}

# Chat

@app.post("/chat")
async def chat(data: Message):

    pregunta = data.message

    # Convertir Sheet a texto

    datos = df.to_string()

    # OpenAI

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
                Eres EMPRETUR IA.

                Responde usando la información del Google Sheet.

                Datos disponibles:

                {datos}

                Responde claro y profesionalmente.
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
