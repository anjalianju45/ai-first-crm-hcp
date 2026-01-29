from sqlalchemy import Column, Integer, String
from database import Base

class HCPInteraction(Base):
    __tablename__ = "hcp_interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String)
    interaction_date = Column(String)
    notes = Column(String)
    sentiment = Column(String)
    follow_up = Column(String)
