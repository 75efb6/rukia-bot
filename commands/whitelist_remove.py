import nextcord
from nextcord.ext import commands
from handlers.apirequests import DroidAPI
import config


class WhitelistRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="whitelist_remove",
        description="Command to remove beatmaps from the whitelist.",
        guild_ids=[config.guild_id],
    )
    async def _whitelist_remove(
        self,
        interaction: nextcord.Interaction,
        setid: int = nextcord.SlashOption(
            description="Numerical ID of the map you want to remove from WL."
        ),
    ):
        role_id = config.wl_roleid
        role = interaction.guild.get_role(role_id)
        ## Checking if role exists.
        if role is None:
            await interaction.response.send_message(
                "The specified role does not exist in this server.", ephemeral=True
            )
            return
        ## Checking if user has role
        if role not in interaction.user.roles:
            await interaction.response.send_message(
                "You do not have the required role to use this command.", ephemeral=True
            )
            return

        await interaction.response.defer()
        ## Requesting map id for each mapset using osu.ppy v1 API
        if DroidAPI().wl_fromset(setid=setid, isAdd=False) is not None:
            await interaction.followup.send("Done.")
        else:
            await interaction.followup.send(
                "Failed to fetch IDs from the first API."
            )


def setup(bot):
    if bot.get_cog("WhitelistRemove") is None:
        bot.add_cog(WhitelistRemove(bot))
