from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.user import User
from services.security import hash_password, verify_password, create_access_token
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from services.security import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/api/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# -------- SCHEMAS LOCAUX --------
class RegisterSchema(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    password: str
    niveau: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

# -------- DB DEP --------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------- REGISTER --------
@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    user = User(
        nom=data.nom,
        prenom=data.prenom,
        email=data.email,
        password=hash_password(data.password),
        niveau=data.niveau
    )

    db.add(user)
    db.commit()
    return {"message": "Compte créé avec succès"}

# -------- LOGIN --------
@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    token = create_access_token({
        "sub": user.email,
        "role": user.role
    })

    return {
        "access_token": token,
        "user": {
            "nom": user.nom,
            "prenom": user.prenom,
            "email": user.email,
            "niveau": user.niveau,
            "role": user.role
        }
    }
# -------- CURRENT USER --------
@router.get("/me")
def get_me(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Token invalide")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    return {
        "id": user.id,
        "nom": user.nom,
        "prenom": user.prenom,
        "email": user.email,
        "niveau": user.niveau,
        "role": user.role
    }
