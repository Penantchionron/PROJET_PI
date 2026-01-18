from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

# --- CLASSE USER ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    niveau = Column(String(20), nullable=False)
    role = Column(String(20), default="student")

    # Relation avec Chat (1 User -> N Chats)
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")
    # Relation avec Message (1 User -> N Messages)
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")