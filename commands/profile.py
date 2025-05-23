import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from typing import Optional
from handlers.mongodb import mongodb_handler
from handlers.apirequests import DroidAPI
import config


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="profile", description="Responds with the info of the specified user."
    )
    async def _profile(
        self,
        interaction: nextcord.Interaction,
        uid: Optional[int] = SlashOption(
            required=False, description="Numerical ID of the user you want."
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
        profile = DroidAPI().get_profile(uid=user_id)
        if profile is not None:
            embed = nextcord.Embed(
                description=f"**▸ Global Rank: #{profile.rank}**\n**▸ PP:** {profile.pp} **Accuracy:** {round(profile.acc, 2)}%\n**▸ Playcount:** {profile.pc}",
                color=0x00FF00,
            )
            embed.set_thumbnail(url=f"{config.domain}/user/avatar/{user_id}.png")
            embed.set_author(
                icon_url=f"https://flagcdn.com/w20/{str(profile.country).lower()}.png",
                name=profile.user_name,
                url=f"{config.domain}/user/profile.php?id={user_id}",
            )
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("Couldn't fetch the data.")


def setup(bot):
    if bot.get_cog("profile") is None:
        bot.add_cog(Profile(bot))
