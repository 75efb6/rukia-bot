import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from typing import Optional
from handlers.mongodb import mongodb_handler
from handlers.apirequests import DroidAPI, OsuAPI


class Recent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="recent",
        description="Responds with the recent play of the specified user.",
    )
    async def _recent(
        self,
        interaction: nextcord.Interaction,
        uid: Optional[int] = SlashOption(
            required=False, description="Numerical ID of the user you want."
        ),
        index: Optional[int] = SlashOption(
            required=False,
            default=0,
            description="Index of the play you want to get (Default = 0)",
        ),
    ):
        await interaction.response.defer()
        ## Check if user has account binded and if user has specified an UID in the command options
        if uid is None:
            d_id = str(interaction.user.id)
            u_data = mongodb_handler.get_profile(d_id)
            try:
                user_id = u_data.get("uid")
            except Exception:
                await interaction.followup.send(
                    "You didn't specify an UID, and you don't have any account binded."
                )
                return
        else:
            user_id = uid
        ## Calling API for user info
        recent = DroidAPI().get_recent(uid=user_id, index=index)
        if recent is not None:
            m = OsuAPI().get_mapdata_fromhash(hash=recent.maphash)
            if m is None:
                return await interaction.followup.send(
                    "Map doesn't exist on osu.ppy.sh"
                )
            status = DroidAPI().get_status(hash=recent.maphash)
            ## Sending the embed
            embed = nextcord.Embed(
                description=f"▸ {recent.rank} ▸ {round(recent.pp, 2)}pp ▸ {round(recent.acc, 2)}%\n▸ {recent.score} ▸ x{recent.combo}/{m.max_combo}\n▸ 300: {recent.h300}x | 100: {recent.h100}x | 50: {recent.h50}x | X: {recent.hmiss}x",
                color=0x00FF00,
            )
            embed.set_author(
                icon_url=status,
                name=f"☆ {round(m.sr, 2)} {m.artist} - {m.title} [{m.version}] +{recent.mods}",
                url=f"https://osu.ppy.sh/beatmapsets/{m.setid}#osu/{m.diffid}",
            )
            embed.set_thumbnail(url=f"https://b.ppy.sh/thumb/{m.setid}l.jpg")
            await interaction.followup.send(
                embed=embed,
                content=f"Recent play for UID: {user_id} (Index: {index})",
            )
        else:
            await interaction.followup.send("Couldn't fetch recent data.")


def setup(bot):
    if bot.get_cog("recent") is None:
        bot.add_cog(Recent(bot))
