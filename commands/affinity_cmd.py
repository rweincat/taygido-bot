import discord
from discord import app_commands

from core.affinity import get_affinity

# -----------------------------
# 호감도 텍스트 변환
# -----------------------------

def get_affinity_text(value: int) -> str:

    if value >= 80:
        return "타기도 좋아... 🌸"

    if value >= 50:
        return "타기타기!! ✨"

    if value >= 20:
        return "타기!"

    if value >= 0:
        return "타기."

    return "타기..."

# -----------------------------
# 슬래시 커맨드 등록
# -----------------------------

def register_affinity_command(bot):

    @bot.tree.command(
        name="호감도",
        description="현재 타기 호감도를 확인해요!"
    )
    async def affinity_command(
        interaction: discord.Interaction
    ):

        user_id = str(interaction.user.id)

        affinity = get_affinity(user_id)

        mood_text = get_affinity_text(affinity)

        embed = discord.Embed(
            title="💖 타기 호감도",
            description=(
                f"{interaction.user.mention}\n\n"
                f"현재 호감도: `{affinity}`\n"
                f"{mood_text}"
            ),
            color=discord.Color.pink()
        )

        await interaction.response.send_message(
            embed=embed
        )