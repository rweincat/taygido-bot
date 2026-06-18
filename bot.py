import discord
import random
from discord.ext import commands

from config import TOKEN

from llm.analyzer import analyze_message
from core.responder import generate_taygi_response
from core.affinity import update_affinity

from commands.affinity_cmd import register_affinity_command
from commands.ranking_cmd import register_ranking_command

# -----------------------------
# intents
# -----------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# -----------------------------
# trigger
# -----------------------------

def has_trigger(text: str) -> bool:
    return "타기" in text.lower().replace(" ", "")

# -----------------------------
# ready
# -----------------------------

@bot.event
async def on_ready():
    print(f"[READY] Logged in as {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"[SYNC] {len(synced)} slash commands synced")
    except Exception as e:
        print(f"[ERROR] Slash sync failed: {e}")

# -----------------------------
# 질문 판정
# -----------------------------

YES_NO_HINTS = [
    "야?", "냐?", "임?", "인가?", "돼?", "되?",
    "맞아?", "해?", "했어?", "있어?", "없어?"
]

def is_question(text: str, analysis: dict):

    t = text.strip()

    is_yesno = any(h in t for h in YES_NO_HINTS)

    is_general = (
        "?" in t or analysis.get("question", False)
    )

    return {
        "is_yesno": is_yesno,
        "is_general": is_general,
        "is_question": is_yesno or is_general
    }

# -----------------------------
# 강도 계산
# -----------------------------

def calculate_intensity(text: str, analysis: dict) -> int:
    score = 1

    if analysis.get("is_rude"):
        score += 3
    if analysis.get("negative"):
        score += 2
    if analysis.get("positive"):
        score += 1
    if analysis.get("is_affection"):
        score += 2

    score += len(text) // 60
    score += text.count("!")
    score += text.count("?")

    return max(1, min(score, 10))

# -----------------------------
# reaction
# -----------------------------

def pick_reaction(analysis: dict, qinfo: dict, text: str):

    t = text.strip()

    if qinfo["is_yesno"]:
        return random.choice(["✔️", "❌"])

    if qinfo["is_general"] and "?" in t:
        return "❓"

    if analysis.get("positive"):
        return random.choice(["✨", "✔️"])

    if analysis.get("negative"):
        return random.choice(["❌", "💢"])

    if analysis.get("is_rude"):
        return random.choice(["💢", "⚠️"])

    if analysis.get("is_confused"):
        return "❓"

    return None

# -----------------------------
# message event
# -----------------------------

@bot.event
async def on_message(message: discord.Message):

    if message.author.bot:
        return

    content = message.content.strip()
    if not content:
        return

    if not has_trigger(content) and bot.user not in message.mentions:
        return

    try:

        analysis = analyze_message(content)
        qinfo = is_question(content, analysis)

        if analysis.get("is_rude") and random.random() < 0.2:
            return

        intensity = calculate_intensity(content, analysis)

        raw_delta = analysis.get("affection_delta", 0)

        # -----------------------------
        # 🔥 핵심 수정
        # -----------------------------

        try:
            raw_delta = int(raw_delta)
        except:
            raw_delta = 0

        real_delta = int(raw_delta * intensity)

        # 너무 큰 값 방지
        real_delta = max(-50, min(real_delta, 50))

        new_affinity = None

        # 0이면 DB 안 건드림
        if real_delta != 0:
            new_affinity = update_affinity(
                str(message.author.id),
                real_delta
            )

            print(f"[AFFINITY] {message.author.id}: {real_delta} -> {new_affinity}")

        async with message.channel.typing():

            response = generate_taygi_response(
                analysis=analysis,
                affinity=new_affinity if new_affinity is not None else 0,
                username=message.author.display_name,
                user_message=content
            )

        if response and real_delta != 0:

            tag = f"`♥️+{real_delta}`" if real_delta > 0 else f"`💔{real_delta}`"
            response = f"{response}\n{tag}"

        if response:
            await message.reply(response, mention_author=False)

        try:
            reaction = pick_reaction(analysis, qinfo, content)

            if reaction and random.random() < 0.5:
                await message.add_reaction(reaction)

        except:
            pass

    except Exception as e:
        print(f"[MESSAGE ERROR] {e}")

    await bot.process_commands(message)

# -----------------------------
# slash commands
# -----------------------------

register_affinity_command(bot)
register_ranking_command(bot)

# -----------------------------
# run
# -----------------------------

bot.run(TOKEN)