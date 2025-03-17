import nextcord
from nextcord.ext import commands
from handlers.apirequests import DroidAPI
import config


class WhitelistAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="whitelist_add",
        description="Command to add beatmaps to the whitelist.",
        guild_ids=[config.guild_id],
    )
    async def _whitelist_add(
        self,
        interaction: nextcord.Interaction,
        setid: int = nextcord.SlashOption(
            description="Numerical ID of the map you want to add to the WL."
        ),
    ):
        role_id = config.wl_roleid
        role = interaction.guild.get_role(role_id)
        ## Checking if role exists in server
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
        if DroidAPI().wl_fromset(setid=setid, isAdd=True) is not None:
            await interaction.followup.send("Done.")
        else:
            await interaction.followup.send(
                "Failed to fetch IDs from the first API."
            )


def setup(bot):
    if bot.get_cog("WhitelistAdd") is None:
        bot.add_cog(WhitelistAdd(bot))
