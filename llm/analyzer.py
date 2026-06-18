import json

from llm.ollama_client import generate_llm_response

# -----------------------------
# 기본 fallback
# -----------------------------

DEFAULT_ANALYSIS = {

    "emotion": "neutral",

    "question": False,

    "positive": False,
    "negative": False,

    "is_rude": False,
    "is_praise": False,
    "is_affection": False,
    "is_greeting": False,
    "is_confused": False,

    "affection_delta": 0,

    "reaction": None,

    "reply_emojis": []
}

# -----------------------------
# 메시지 분석
# -----------------------------

def analyze_message(message: str) -> dict:

    prompt = f"""
You are a STRICT emotion + behavior classifier for a Discord mascot AI.

You MUST return ONLY valid JSON.
NO explanations.
NO markdown.
NO extra text.

========================
IMPORTANT GLOBAL RULES
========================

1. NEVER overuse "angry"

- "angry" is ONLY for clear insults, hate, or aggressive behavior
- NOT for jokes, sarcasm, short messages, or neutral complaints

2. If you are unsure → ALWAYS choose "neutral"
NEVER default to "angry"

3. Normal conversation is usually:
neutral, happy, greeting, embarrassed
NOT angry

4. Consistency rule:
- If is_rude = false → emotion MUST NOT be "angry"
- If emotion = "angry" → is_rude MUST be true

========================
EMOTIONS
========================

- happy
- sad
- angry
- embarrassed
- greeting
- praise
- neutral

========================
BEHAVIOR FLAGS
========================

question:
- true if asking anything or ending with ?

positive:
- kindness, compliments, friendly tone

negative:
- insult, hate, aggression

is_rude:
- only for real insults, hate, hostility

is_praise:
- compliments, admiration

is_affection:
- cute, love, emotional attachment

is_greeting:
- hello, hi, hey

is_confused:
- unclear intent, asking help

========================
REACTION RULES
========================

QUESTION:
❓

HAPPY:
✨ 💕 🌸

SAD:
🥺 💧

GREETING:
👋 ✨

PRAISE:
✨ 💕 🌸 💖

AFFECTION:
💞 💕

CONFUSED:
❓ 😵

ANGRY:
💢 ❌ 😡 💥 ⚠️

========================
AFFECTION RULES
========================

+3 very positive
+2 positive
+1 neutral positive
0 neutral
-1 slight rude
-3 rude
-5 very rude

========================
REPLY EMOJIS (0~2)
========================

Examples:
["✨"]
["💢"]
["🥺"]
["💞","✨"]
[]

========================
OUTPUT FORMAT
========================

{{
    "emotion": "neutral",
    "question": false,

    "positive": false,
    "negative": false,

    "is_rude": false,
    "is_praise": false,
    "is_affection": false,
    "is_greeting": false,
    "is_confused": false,

    "affection_delta": 0,

    "reaction": null,

    "reply_emojis": []
}}

========================
USER MESSAGE
========================

\"\"\"{message}\"\"\"
"""

    try:

        raw_response = generate_llm_response(prompt)

        # -----------------------------
        # JSON 추출
        # -----------------------------

        start = raw_response.find("{")
        end = raw_response.rfind("}") + 1

        if start == -1 or end == 0:
            return DEFAULT_ANALYSIS

        data = json.loads(raw_response[start:end])

        # -----------------------------
        # emotion 안전화
        # -----------------------------

        emotion = data.get("emotion", "neutral")

        valid_emotions = {
            "happy",
            "sad",
            "angry",
            "embarrassed",
            "greeting",
            "praise",
            "neutral"
        }

        if emotion not in valid_emotions:
            emotion = "neutral"

        # -----------------------------
        # 🔥 consistency 보정 (핵심)
        # -----------------------------

        is_rude = bool(data.get("is_rude", False))

        if not is_rude and emotion == "angry":
            emotion = "neutral"

        if emotion == "angry":
            is_rude = True

        # -----------------------------
        # return
        # -----------------------------

        return {

            "emotion": emotion,

            "question": bool(data.get("question", False)),

            "positive": bool(data.get("positive", False)),
            "negative": bool(data.get("negative", False)),

            "is_rude": is_rude,
            "is_praise": bool(data.get("is_praise", False)),
            "is_affection": bool(data.get("is_affection", False)),
            "is_greeting": bool(data.get("is_greeting", False)),
            "is_confused": bool(data.get("is_confused", False)),

            "affection_delta": int(data.get("affection_delta", 0)),

            "reaction": data.get("reaction", None),

            "reply_emojis": data.get("reply_emojis", [])
        }

    except Exception as e:

        print(f"[ANALYZER ERROR] {e}")

        return DEFAULT_ANALYSIS