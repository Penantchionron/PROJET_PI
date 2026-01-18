from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from db.database import SessionLocal
from models.chat import Chat
from models.message import Message
from models.user import User
from services.security import get_current_user
from services.llm import (
    generate_ai_response,
    clean_ai_output,
    generate_chat_title,
    generate_math_image,
)
from services.rag import get_relevant_context

router = APIRouter(prefix="/api/chat", tags=["Chat"])

# ==============================
# DB DEPENDENCY
# ==============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==============================
# SCHEMAS (Pydantic)
# ==============================
class ChatCreateSchema(BaseModel):
    title: str | None = "Nouveau chat"

class MessageCreateSchema(BaseModel):
    content: str

class MessageResponseSchema(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatResponseSchema(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True

# ==============================
# ROUTES CHAT
# ==============================
@router.post("", response_model=ChatResponseSchema)
def create_chat(
    data: ChatCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = Chat(title=data.title, user_id=current_user.id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

@router.get("", response_model=List[ChatResponseSchema])
def list_my_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Chat)
        .filter(Chat.user_id == current_user.id)
        .order_by(Chat.created_at.desc())
        .all()
    )

@router.get("/{chat_id}/messages", response_model=List[MessageResponseSchema])
def get_chat_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat introuvable")

    return (
        db.query(Message)
        .filter(Message.chat_id == chat.id)
        .order_by(Message.created_at.asc())
        .all()
    )

# ==============================
# LOGIQUE IA & MESSAGES
# ==============================
@router.post("/{chat_id}/message", response_model=List[MessageResponseSchema])
def send_message(
    chat_id: int,
    data: MessageCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Vérification du chat
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat introuvable")

    # 2. Enregistrement du message utilisateur
    user_msg = Message(
        chat_id=chat.id,
        role="user",
        content=data.content,
        user_id=current_user.id
    )
    db.add(user_msg)

    # 3. Mise à jour automatique du titre si nécessaire
    if chat.title == "Nouveau chat":
        chat.title = generate_chat_title(data.content)

    # 4. RAG & Analyse de niveau
    context = get_relevant_context(data.content, current_user.niveau)
    
    niveau_map = {"6ème": 6, "5ème": 5, "4ème": 4, "3ème": 3}
    user_level_num = niveau_map.get(current_user.niveau, 6)

    # Logique de filtrage (Améliorée)
    question_is_maths = len(data.content.split()) > 1 # Simple check ou basé sur le retour RAG
    
    # Détection simplifiée du hors-niveau (ex: si le contexte mentionne un niveau plus petit numériquement)
    # Note: En Côte d'Ivoire, 3ème < 6ème en chiffre mais niveau 3ème > 6ème.
    # On inverse la logique si nécessaire.
    question_out_of_level = False
    if "niveau 3ème" in context.lower() and current_user.niveau == "6ème":
        question_out_of_level = True

    # 5. Construction du Prompt
    if not question_is_maths:
        prompt = f"Réponds poliment que tu es un prof de maths et que tu ne peux répondre qu'aux questions de mathématiques. Question: {data.content}"
    elif question_out_of_level:
        prompt = f"L'élève est en {current_user.niveau}. La question semble trop complexe. Explique les bases liées à cette question adaptées à son niveau. Contexte: {context} Question: {data.content}"
    else:
        prompt = f"""Tu es un professeur de mathématiques sérieux (Programme Ivoirien). 
Niveau de l'élève: {current_user.niveau}.
Règles: Pas de blabla, pas de salutations.
Structure: EXPLICATION, EXEMPLE, EXERCICE, CORRECTION.
CONTEXTE: {context}
QUESTION: {data.content}"""

    # 6. Génération et nettoyage
    try:
        ai_text = generate_ai_response(prompt)
        ai_text = clean_ai_output(ai_text)

        # Gestion de l'image
        if "<IMG>" in ai_text:
            img_url = generate_math_image(data.content)
            ai_text = ai_text.replace("<IMG>", f"![figure]({img_url})")

        # 7. Enregistrement du message assistant
        assistant_msg = Message(
            chat_id=chat.id,
            role="assistant",
            content=ai_text,
            user_id=None # L'assistant n'a pas d'ID User
        )
        db.add(assistant_msg)
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la génération de la réponse")

    # 8. Retour de l'historique complet
    return (
        db.query(Message)
        .filter(Message.chat_id == chat.id)
        .order_by(Message.created_at.asc())
        .all()
    )