from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

# --- CLASSE MESSAGE ---
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(20))  # user | assistant
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relation inverse vers User
    user = relationship("User", back_populates="messages")
    # Relation inverse vers Chat
    # Correction ici : back_populates="messages" (au pluriel pour correspondre à la classe Chat)
    chat = relationship("Chat", back_populates="messages")