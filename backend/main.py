from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import engine, SessionLocal
from models import Base, HCPInteraction
from schemas import InteractionCreate, InteractionResponse, ChatRequest


app = FastAPI(title="AT-First CRM-HCP")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.post("/interactions", response_model=InteractionResponse)
def create_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    obj = HCPInteraction(**interaction.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/interactions", response_model=list[InteractionResponse])
def get_interactions(db: Session = Depends(get_db)):
    return db.query(HCPInteraction).all()

import re

@app.post("/chat")
def chat(chat: ChatRequest):
    text = chat.message

    # ---------- NAME ----------
    name_match = re.search(r"dr\s+([a-zA-Z]+)", text, re.IGNORECASE)
    hcp_name = f"Dr {name_match.group(1)}" if name_match else "Dr Unknown"

    # ---------- DATE ----------
    date_match = re.search(r"\d{2}-\d{2}-\d{4}", text)
    interaction_date = date_match.group(0) if date_match else ""

    # ---------- SENTIMENT ----------
    if "positive" in text.lower():
        sentiment = "Positive"
    elif "negative" in text.lower():
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # ---------- FOLLOW UP ----------
    follow_up = ""
    if "brochure" in text.lower():
        follow_up = "Send brochure"
    elif "call" in text.lower():
        follow_up = "Schedule follow-up call"
    elif "email" in text.lower():
        follow_up = "Send email"
    elif "meeting" in text.lower():
        follow_up = "Schedule meeting"

    return {
        "hcp_name": hcp_name,
        "interaction_date": interaction_date,
        "notes": chat.message,
        "sentiment": sentiment,
        "follow_up": follow_up
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
