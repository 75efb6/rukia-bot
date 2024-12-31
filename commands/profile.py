import nextcord
import config
from nextcord.ext import commands
from nextcord import SlashOption
import aiohttp
from typing import Optional
from handlers.mongodb import mongodb_handler

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="profile", description="Responds with the info of the specified user.")
    async def _profile(self, interaction: nextcord.Interaction, uid: Optional[int] = SlashOption(required=False)):
        if uid == False:
            d_id= str(interaction.user.id)
            u_data = mongodb_handler.get_profile(d_id)
            uid = u_data.get("$uid", "N/A")
        ## Calling API for user info
        async with aiohttp.ClientSession() as session:
            api_url = f'http://{config.domain}/api/get_user?id={uid}'
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    ## Parsing the data
                    user_name = data.get('name', 'N/A')
                    stats = data.get('stats', 'N/A')
                    rank = stats.get('rank', 'N/A')
                    pp = stats.get('pp', "N/A")
                    acc = stats.get('accuracy', 'N/A')
                    pc = stats.get('plays', 'N/A')

                    embed = nextcord.Embed(title=f"User Profile for user: {user_name}", description=f"**Global Rank: #{rank}**", color=0x00ff00)
                    embed.set_thumbnail(url=f"http://{config.domain}/user/avatar/{uid}.png")
                    embed.add_field(name="Accuracy:", value=f"{round(acc, 2)}%", inline=False)
                    embed.add_field(name="Performance Points:", value=f"{pp}pp", inline=False)
                    embed.add_field(name="Playcount:", value=f"{pc} plays")
                    
                    await interaction.response.send_message(embed=embed)

                else:
                    await interaction.response.send_message("Couldn't fetch the data.")

def setup(bot):
    if bot.get_cog("profile") is None:
        bot.add_cog(Profile(bot))
