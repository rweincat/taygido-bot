import discord

from core.affinity import get_top_affinity

# -----------------------------
# 호감도 등급 텍스트
# -----------------------------

def get_rank_emoji(score: int) -> str:

    if score >= 80:
        return "🌸"

    if score >= 50:
        return "✨"

    if score >= 20:
        return "💖"

    if score >= 0:
        return "🙂"

    return "💀"

# -----------------------------
# 슬래시 커맨드 등록
# -----------------------------

def register_ranking_command(bot):

    @bot.tree.command(
        name="랭킹",
        description="타기 호감도 랭킹을 확인해요!"
    )
    async def ranking_command(
        interaction: discord.Interaction
    ):

        ranking = get_top_affinity(10)

        if not ranking:

            await interaction.response.send_message(
                "타기..."
            )

            return

        lines = []

        for idx, (user_id, score) in enumerate(ranking, start=1):

            member = interaction.guild.get_member(
                int(user_id)
            )

            username = (
                member.display_name
                if member
                else f"Unknown User ({user_id})"
            )

            emoji = get_rank_emoji(score)

            lines.append(
                f"`#{idx}` {emoji} "
                f"**{username}** - `{score}`"
            )

        embed = discord.Embed(
            title="🏆 타기 호감도 랭킹",
            description="\n".join(lines),
            color=discord.Color.gold()
        )

        await interaction.response.send_message(
            embed=embed
        )