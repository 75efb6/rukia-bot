import nextcord
from nextcord.ext import commands
from handlers.apirequests import DroidAPI
import config


class WhitelistRemoveDiff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="whitelist_rmdiff",
        description="Command to remove difficulties of a certain beatmap from the whitelist.",
        guild_ids=[config.guild_id],
    )
    async def _whitelist_rmdiff(
        self,
        interaction: nextcord.Interaction,
        diffid: int = nextcord.SlashOption(
            description="Numerical ID of the difficulty you want to remove from WL."
        ),
    ):
        ## Checking if role exists and user has role
        role_id = config.wl_roleid
        role = interaction.guild.get_role(role_id)

        if role is None:
            await interaction.response.send_message(
                "The specified role does not exist in this server.", ephemeral=True
            )
            return

        if role not in interaction.user.roles:
            await interaction.response.send_message(
                "You do not have the required role to use this command.", ephemeral=True
            )
            return

        await interaction.response.defer()

        if DroidAPI().wl_fromid(mapid=diffid, isAdd=False) is not None:
            await interaction.followup.send("Done.")
        else:
            await interaction.followup.send(
                "Failed to fetch IDs from the first API."
            )


def setup(bot):
    if bot.get_cog("WhitelistRemoveDiff") is None:
        bot.add_cog(WhitelistRemoveDiff(bot))
