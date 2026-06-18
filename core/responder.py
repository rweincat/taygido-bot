import random
from core.rarity import get_rare_response

# -----------------------------
# 기본 단어
# -----------------------------

BASE_WORDS = [
    "타기",
    "타기도",
    "타기타기",
    "타기이",
    "타..."
]

# -----------------------------
# 감정 스타일
# -----------------------------

EMOTION_STYLES = {

    "happy": {
        "suffix": ["!!", "~", "!! ✨", "~ ✨", "!! 🌸"],
        "emoji": ["✨", "🌸", "💕"],
        "repeat": (2, 4)
    },

    "sad": {
        "suffix": ["...", "..", "... 🥺"],
        "emoji": ["🥺"],
        "repeat": (1, 2)
    },

    "angry": {
        "suffix": ["!!", "...!", "!! 💢"],
        "emoji": ["💢", "❌", "😡"],
        "repeat": (3, 5)
    },

    "embarrassed": {
        "suffix": ["...", ".. 🌸", "~"],
        "emoji": ["🌸", "💕"],
        "repeat": (1, 2)
    },

    "greeting": {
        "suffix": ["!", "~", "!! ✨"],
        "emoji": ["✨"],
        "repeat": (1, 3)
    },

    "praise": {
        "suffix": ["!!", "~ ✨", "!! 🌸"],
        "emoji": ["✨", "💕", "🌸"],
        "repeat": (2, 4)
    },

    "neutral": {
        "suffix": [".", "...", "~"],
        "emoji": [],
        "repeat": (1, 2)
    }
}

# -----------------------------
# 질문 suffix
# -----------------------------

QUESTION_SUFFIXES = ["?", "...?", "~?"]

# -----------------------------
# 안전 문자
# -----------------------------

ALLOWED_CHARS = set(
    "타기도이...?!~✨🌸💕🥺💢❌😡❓👋 "
)

def sanitize(text: str) -> str:
    cleaned = "".join(ch for ch in text if ch in ALLOWED_CHARS)
    return cleaned.strip() or "타기..."

# -----------------------------
# 길이 보정
# -----------------------------

def length_bonus(msg: str) -> int:
    l = len(msg)
    if l >= 150: return 4
    if l >= 80: return 3
    if l >= 40: return 2
    if l >= 20: return 1
    return 0

# -----------------------------
# 단어 생성
# -----------------------------

def build_words(n: int) -> str:
    return " ".join(random.choice(BASE_WORDS) for _ in range(n))

# -----------------------------
# 질문 판정 (개선)
# -----------------------------

QUESTION_HINTS = ["뭐", "왜", "어디", "어떻게", "언제", "가능", "맞아", "해"]

def is_real_question(text: str) -> bool:
    t = text.strip()

    # 강한 질문
    if "?" in t:
        return True

    # 의문사 + 짧은 문장
    if any(w in t for w in QUESTION_HINTS) and len(t) < 80:
        return True

    return False

# -----------------------------
# override (확률형으로 변경)
# -----------------------------

def handle_llm_override(analysis: dict):

    # 🔥 70%만 발동 (중요)
    if random.random() > 0.7:
        return None

    if analysis.get("is_rude"):

        return random.choice([
            "타기...",
            "타기도... 💢",
            "타기이!! 💢"
        ])

    if analysis.get("is_praise"):

        emojis = analysis.get("reply_emojis", ["✨"])
        return "타기타기!! " + " ".join(emojis[:2])

    if analysis.get("is_affection"):

        emojis = analysis.get("reply_emojis", ["💕"])
        return "타기도... " + " ".join(emojis[:2])

    if analysis.get("is_confused"):

        return random.choice([
            "타기...?",
            "타기이?",
            "타기도...?"
        ])

    return None

# -----------------------------
# 일반 응답
# -----------------------------

def build_response(emotion, is_question, affinity, user_message, analysis):

    style = EMOTION_STYLES.get(emotion, EMOTION_STYLES["neutral"])

    repeat = random.randint(*style["repeat"])
    repeat += length_bonus(user_message)

    if affinity >= 50:
        repeat += 1
    if affinity >= 80:
        repeat += 1

    repeat = min(repeat, 10)

    text = build_words(repeat)

    # -----------------------------
    # 질문 처리 (자연스럽게)
    # -----------------------------

    if is_question:

        # ❗ 항상 ? 붙이지 않음 (핵심 개선)
        if random.random() < 0.6:
            text += random.choice(QUESTION_SUFFIXES)

    else:
        text += random.choice(style["suffix"])

    # -----------------------------
    # emoji
    # -----------------------------

    reply_emojis = analysis.get("reply_emojis", [])

    if reply_emojis and random.random() < 0.5:
        text += " " + " ".join(reply_emojis[:2])

    elif style["emoji"] and random.random() < 0.25:
        text += " " + random.choice(style["emoji"])

    return sanitize(text)

# -----------------------------
# 메인
# -----------------------------

def generate_taygi_response(analysis, affinity, username="", user_message=""):

    emotion = analysis.get("emotion", "neutral")

    is_question = is_real_question(user_message)

    rare = get_rare_response(emotion, affinity)
    if rare:
        return sanitize(rare)

    override = handle_llm_override(analysis)
    if override:
        return sanitize(override)

    return build_response(
        emotion,
        is_question,
        affinity,
        user_message,
        analysis
    )