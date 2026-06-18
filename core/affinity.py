import json
import os

from config import (
    AFFINITY_FILE,
    DEFAULT_AFFINITY,
    MAX_AFFINITY,
    MIN_AFFINITY
)

# -----------------------------
# 파일 초기화
# -----------------------------

def ensure_affinity_file():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(AFFINITY_FILE):

        with open(
            AFFINITY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump({}, f)

# -----------------------------
# 데이터 로드
# -----------------------------

def load_affinity_data():

    ensure_affinity_file()

    with open(
        AFFINITY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

# -----------------------------
# 데이터 저장
# -----------------------------

def save_affinity_data(data):

    with open(
        AFFINITY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )

# -----------------------------
# 호감도 가져오기
# -----------------------------

def get_affinity(user_id: str) -> int:

    data = load_affinity_data()

    return data.get(
        user_id,
        DEFAULT_AFFINITY
    )

# -----------------------------
# 호감도 수정
# -----------------------------

def update_affinity(
    user_id: str,
    delta: int
) -> int:

    data = load_affinity_data()

    current = data.get(
        user_id,
        DEFAULT_AFFINITY
    )

    updated = current + delta

    # 범위 제한
    updated = max(
        MIN_AFFINITY,
        min(MAX_AFFINITY, updated)
    )

    data[user_id] = updated

    save_affinity_data(data)

    return updated

# -----------------------------
# 호감도 직접 설정
# -----------------------------

def set_affinity(
    user_id: str,
    value: int
):

    data = load_affinity_data()

    value = max(
        MIN_AFFINITY,
        min(MAX_AFFINITY, value)
    )

    data[user_id] = value

    save_affinity_data(data)

# -----------------------------
# 호감도 랭킹
# -----------------------------

def get_top_affinity(limit: int = 10):

    data = load_affinity_data()

    sorted_users = sorted(
        data.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_users[:limit]