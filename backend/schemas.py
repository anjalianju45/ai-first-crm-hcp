from pydantic import BaseModel

class InteractionCreate(BaseModel):
    hcp_name: str
    interaction_date: str
    notes: str
    sentiment: str
    follow_up: str

class InteractionResponse(InteractionCreate):
    id: int

class ChatRequest(BaseModel):
    message: str
