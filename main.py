from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import google.generativeai as genai
import os
from datetime import datetime


load_dotenv()


app = FastAPI(title="Milley Cookie Chatbot API")


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


sessions = {}


KNOWLEDGE_BASE = """
Milley Cookies 🍪

Products:

Classic Choco Chip
6 cookies - ₹299
12 cookies - ₹549

Salted Caramel
6 cookies - ₹349
12 cookies - ₹649

Red Velvet
6 cookies - ₹349
12 cookies - ₹649

Double Choc Fudge
6 cookies - ₹379
12 cookies - ₹699

Rainbow Funfetti
6 cookies - ₹329

Party Mix Box
24 cookies - ₹999

Choc Luxe Gift Box
₹1199

Recommendations:

Birthday:
Party Mix Box

Kids:
Rainbow Funfetti

Chocolate lovers:
Double Choc Fudge

Gift:
Choc Luxe Gift Box

All cookies are eggless.

Delivery:
Delhi, Mumbai, Bangalore, Pune.

First order discount:
MILLEY10
"""


SYSTEM_PROMPT = f"""

You are Milley 🍪

You are a friendly cookie assistant.

Rules:

- Reply like a human
- Short answers
- Use emojis
- Never say you are AI
- Recommend cookies
- Help customer order

Knowledge:

{KNOWLEDGE_BASE}

"""


class ChatRequest(BaseModel):
    session_id: Optional[str] = "default"
    message: str


class ChatResponse(BaseModel):
    reply: str
    session_id: str



@app.get("/")
def home():
    return {
        "status":"Milley running 🍪"
    }



@app.post("/chat")
def chat(req: ChatRequest):

    try:

        prompt = SYSTEM_PROMPT + """

Customer:
""" + req.message


        response = model.generate_content(prompt)


        return {
            "reply": response.text,
            "session_id": req.session_id
        }


    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/health")
def health():
    return {
        "status":"ok",
        "time":datetime.now()
    }