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
        m = OsuAPI().get_mapdata_fromhash(hash=recent.maphash)
        if recent is not None:
            ## Sending the embed
            embed = nextcord.Embed(
                title=f"☆ {round(m.sr, 2)} {m.artist} - {m.title} [{m.version}] +{recent.mods}",
                url=f"https://osu.ppy.sh/beatmapsets/{m.setid}#osu/{m.diffid}",
                color=0x00FF00,
            )
            embed.set_thumbnail(
                url=f"https://b.ppy.sh/thumb/{m.setid}l.jpg"
            )
            embed.add_field(name="PP:", value=f"{round(recent.pp)}pp")
            embed.add_field(name="Acc:", value=f"{round(recent.acc, 2)}%")
            embed.add_field(
                name="Combo:", value=f"{recent.combo}/{m.max_combo}x"
            )
            embed.add_field(
                name="Judgements:",
                value=f"300: {recent.h300}x | 100: {recent.h100}x | 50: {recent.h50}x | X: {recent.hmiss}x",
                inline=True,
            )
            await interaction.followup.send(
                embed=embed,
                content=f"Recent play for UID: {user_id} (Index: {index})",
            )
        else:
            await interaction.followup.send("Couldn't fetch map data, maybe map isn't submitted on osu! website")

def setup(bot):
    if bot.get_cog("recent") is None:
        bot.add_cog(Recent(bot))
