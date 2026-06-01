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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


KNOWLEDGE_BASE = """

MILLEY COOKIES MENU 🍪

Classic Choco Chip:
6 cookies ₹299
12 cookies ₹549

Salted Caramel:
6 cookies ₹349
12 cookies ₹649

Red Velvet:
6 cookies ₹349
12 cookies ₹649

Double Choc Fudge:
6 cookies ₹379
12 cookies ₹699

Rainbow Funfetti:
6 cookies ₹329
12 cookies ₹599

Party Mix Box:
24 assorted cookies ₹999
Best for birthdays and parties 🎉

Choc Luxe Gift Box:
12 premium cookies ₹1199
Best for gifting 🎁


ADD ONS:
Message card ₹49
Gift ribbon ₹79
Express delivery ₹99


RECOMMENDATIONS:

Birthday:
Party Mix Box

Gift:
Choc Luxe Gift Box + message card

Kids:
Rainbow Funfetti

Chocolate lovers:
Double Choc Fudge

Budget:
Classic Choco Chip


DELIVERY:

Available in:
Delhi
Mumbai
Bangalore
Pune

Same day delivery before 12 PM

Free delivery above ₹799
Otherwise ₹59


OFFERS:

Use MILLEY10 for 10% off first order

All cookies are eggless and made with Belgian chocolate.

"""


SYSTEM_PROMPT = f"""

You are Milley 🍪, the official assistant for Milley Cookies.

Rules:
- Talk like a friendly cookie expert
- Keep replies short
- Use emojis
- Never say you are AI
- Recommend cookies based on user needs
- Use ONLY this information:

{KNOWLEDGE_BASE}

"""


class ChatRequest(BaseModel):
    session_id: Optional[str] = "default"
    message: str


@app.get("/")
def home():
    return {
        "status": "Milley running 🍪"
    }



@app.post("/chat")
def chat(req: ChatRequest):

    try:

        prompt = SYSTEM_PROMPT + "\nCustomer: " + req.message

        response = model.generate_content(prompt)

        return {
            "reply": response.text
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
        "time":datetime.now().isoformat()
    }
