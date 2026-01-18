from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

# --- CLASSE CHAT ---
class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), default="Nouveau chat")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relation inverse vers User
    user = relationship("User", back_populates="chats")
    # Relation vers Message (1 Chat -> N Messages)
    # Correction ici : back_populates="chat" (au singulier pour correspondre à la classe Message)
    messages = relationship("Message", back_populates="chat", cascade="all, delete")
    
    