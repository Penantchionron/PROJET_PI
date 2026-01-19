import os
from google import genai

# ======================================================
# ⚠️ TEST LOCAL UNIQUEMENT
# 👉 METS TA CLÉ ICI POUR TEST
# ======================================================
GEMINI_API_KEY = "API_CLE_ICIC"
# ======================================================

# -----------------------------
# CLIENT FACTORY (IMPORTANT)
# -----------------------------
def _get_gemini_client():
    return genai.Client(
        api_key=GEMINI_API_KEY  
    )

# -----------------------------
# IA PRINCIPALE (CHAT)
# -----------------------------
def generate_ai_response(prompt: str) -> str:
    try:
        client = _get_gemini_client()

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        text = response.text or ""
        return clean_ai_output(text)

    except Exception as e:
        return f"❌ Erreur IA Gemini : {str(e)}"

# -----------------------------
# NETTOYAGE SORTIE IA
# -----------------------------
def clean_ai_output(text: str) -> str:
    forbidden = [
        "RÈGLES",
        "PLAN",
        "Bonjour",
        "Je suis ravi",
        "programme ivoirien",
        "En tant qu'IA",
        "Voici la réponse"
    ]

    for word in forbidden:
        text = text.replace(word, "")

    return text.strip()

# -----------------------------
# TITRE DE CHAT
# -----------------------------
def generate_chat_title(question: str) -> str:
    try:
        client = _get_gemini_client()

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f"Résume cette question de mathématiques en 3 mots maximum : {question}"
        )

        title = response.text or "Discussion math"
        return title.replace(".", "").replace('"', "").strip()[:50]

    except Exception:
        return "Discussion math"

# -----------------------------
# IMAGE (PLACEHOLDER)
# -----------------------------
def generate_math_image(description: str) -> str:
    return (
        "https://via.placeholder.com/400x200.png"
        f"?text={description.replace(' ', '+')}"
    )
