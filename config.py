import os

from dotenv import load_dotenv

# .env 로드
load_dotenv()

# -----------------------------
# Discord
# -----------------------------

TOKEN = os.getenv("TOKEN")

# -----------------------------
# Ollama
# -----------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"

OLLAMA_MODEL = "llama3:8b"

# -----------------------------
# Bot 설정
# -----------------------------

BOT_NAME = "타기"

MAX_MESSAGE_LENGTH = 200

# -----------------------------
# 호감도 설정
# -----------------------------

DEFAULT_AFFINITY = 0

MAX_AFFINITY = 100

MIN_AFFINITY = -20

# -----------------------------
# 희귀 반응 확률
# -----------------------------

RARE_RESPONSE_CHANCE = 0.03

# -----------------------------
# 데이터 파일 경로
# -----------------------------

AFFINITY_FILE = "data/affinity.json"

MEMORY_FILE = "data/memory.json"