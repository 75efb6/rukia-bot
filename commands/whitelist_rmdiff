import nextcord
from nextcord.ext import commands
import aiohttp
import config

class WhitelistRemoveDiff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="whitelist_rmdiff", description="Command to remove difficulties of a certain beatmap from the whitelist. (Limited to users with an specific role.)")
    async def _whitelist_add(self, interaction: nextcord.Interaction, diffid:str):
        role_id = config.wl_roleid
        role = interaction.guild.get_role(role_id)
        
        if role is None:
            await interaction.response.send_message("The specified role does not exist in this server.", ephemeral=True)
            return

        if role not in interaction.user.roles:
            await interaction.response.send_message("You do not have the required role to use this command.", ephemeral=True)
            return
        
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            api_url = f'http://{config.domain}/api/wl_remove?key={config.wl_key}&bid={diffid}'
            async with session.get(api_url) as response:
                if response.status == 200:
                    pass
                else:
                    await interaction.followup.send("Done.")

def setup(bot):
    if bot.get_cog("WhitelistRemoveDiff") is None:
        bot.add_cog(WhitelistRemoveDiff(bot))