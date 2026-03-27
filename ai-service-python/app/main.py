from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = FastAPI()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {
        "message": "AI Service Running 🚀",
        "groq_key_loaded": bool(api_key)
    }


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        user_message = request.message

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        return {
            "response": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "error": str(e)
        }