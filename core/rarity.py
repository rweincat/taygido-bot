import random

from config import RARE_RESPONSE_CHANCE

# -----------------------------
# 희귀 반응 목록
# -----------------------------

RARE_RESPONSES = {

    "happy": [
        "타기타기타기!! ✨",
        "타기이이이!!! 🌸",
        "타기도 좋아!! 💕",
        "타기~!! ✨✨"
    ],

    "sad": [
        "타기이...",
        "타기도 슬퍼...",
        "타기... 🥺",
        "타기..."
    ],

    "angry": [
        "타기!!!",
        "타기이?!",
        "타기....!"
    ],

    "embarrassed": [
        "타기도... 🌸",
        "타기이...",
        "타기.. 💕"
    ],

    "praise": [
        "타기도 좋아... 🌸",
        "타기타기!! 💕",
        "타기~!! ✨"
    ],

    "greeting": [
        "타기타기~!!",
        "타기!!! ✨",
        "타기~ 🌸"
    ],

    "neutral": [
        "타기.",
        "타기...",
        "타기도."
    ]
}

# -----------------------------
# 희귀 반응 가져오기
# -----------------------------

def get_rare_response(
    emotion: str,
    affinity: int
):

    # 확률 실패
    if random.random() > RARE_RESPONSE_CHANCE:
        return None

    # 호감도 높을수록 희귀 확률 증가
    bonus_chance = affinity * 0.001

    if random.random() > bonus_chance + 0.2:
        return None

    responses = RARE_RESPONSES.get(
        emotion,
        RARE_RESPONSES["neutral"]
    )

    return random.choice(responses)