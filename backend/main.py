from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import Base, engine
from api.auth import router as auth_router
from api.chat import router as chat_router

app = FastAPI(title="Math pour tous API")

Base.metadata.create_all(bind=engine)
# from sqlalchemy import text
# with engine.connect() as conn:
#     conn.execute(text("ALTER TABLE messages MODIFY user_id INT NULL"))
#     conn.commit()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(chat_router)

