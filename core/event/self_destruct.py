import asyncio
import discord

# -----------------------------
# 트리거
# -----------------------------

TRIGGER = "타기도 자폭해"

# -----------------------------
# 실행 함수
# -----------------------------

async def run_self_destruct(message: discord.Message) -> bool:
    """
    자폭 이벤트 실행
    반환값:
        True = 실행됨 (메인 로직 중단해야 함)
        False = 실행 안됨
    """

    content = message.content.strip()

    if TRIGGER not in content:
        return False

    try:

        for i in range(5, 0, -1):
            await message.channel.send(str(i))
            await asyncio.sleep(1)

        await message.channel.send("🤖 💥")

    except Exception as e:
        print(f"[SELF DESTRUCT ERROR] {e}")

    return True