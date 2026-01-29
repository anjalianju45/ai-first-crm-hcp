from sqlalchemy.orm import Session
from models import HCPInteraction


def log_interaction_tool(
    db: Session,
    hcp_name: str,
    interaction_date: str = None,
    notes: str = None,
    sentiment: str = None,
    follow_up: str = None,
):
    interaction = HCPInteraction(
        hcp_name=hcp_name,
        interaction_date=interaction_date,
        notes=notes,
        sentiment=sentiment,
        follow_up=follow_up,
    )

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return interaction

def edit_interaction_tool(
    db: Session,
    interaction_id: int,
    notes: str = None,
    sentiment: str = None,
    follow_up: str = None,
):
    interaction = db.query(HCPInteraction).filter(
        HCPInteraction.id == interaction_id
    ).first()

    if not interaction:
        return None

    if notes:
        interaction.notes = notes
    if sentiment:
        interaction.sentiment = sentiment
    if follow_up:
        interaction.follow_up = follow_up

    db.commit()
    db.refresh(interaction)

    return interaction

def summarize_interaction_tool(notes: str):
    if not notes:
        return "No notes provided"

    # Placeholder for LLM
    return f"Summary: {notes[:50]}..."
