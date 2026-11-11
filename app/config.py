"""Configuracion central de Perfilia.

Carga las variables de entorno desde el archivo .env y expone los valores
de configuracion usados por el resto del proyecto.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")

ALLOWED_USER_ID = None
_allowed_user_id_raw = os.getenv("ALLOWED_USER_ID", "")
if _allowed_user_id_raw.strip():
    ALLOWED_USER_ID = int(_allowed_user_id_raw.strip())
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
OUTPUT_LANGUAGE = os.getenv("OUTPUT_LANGUAGE", "es")
MIN_MATCH_SCORE = int(os.getenv("MIN_MATCH_SCORE", "70"))
MAX_FIDELITY_ATTEMPTS = int(os.getenv("MAX_FIDELITY_ATTEMPTS", "3"))

CV_BASE_PATH = BASE_DIR / "cv_base.md"
DATA_DIR = BASE_DIR / "data"
HISTORY_DIR = DATA_DIR / "history"
OUTPUT_DIR = DATA_DIR / "output"
PROMPTS_DIR = BASE_DIR / "prompts"
DB_PATH = HISTORY_DIR / "history.db"

PDF_FONT_REGULAR = Path(os.getenv("PDF_FONT_REGULAR") or "C:/Windows/Fonts/arial.ttf")
PDF_FONT_BOLD = Path(os.getenv("PDF_FONT_BOLD") or "C:/Windows/Fonts/arialbd.ttf")
