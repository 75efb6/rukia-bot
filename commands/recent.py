import nextcord
import config
from nextcord.ext import commands
from nextcord import SlashOption
import aiohttp
from typing import Optional
from handlers.mongodb import mongodb_handler
from handlers.mods import Mods

class Recent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @nextcord.slash_command(name="recent", description="Responds with the recent play of the specified user.")
    async def _recent(self, interaction: nextcord.Interaction, uid: Optional[int] = SlashOption(required=False, description="Numerical ID of the user you want."), index: Optional[int] = SlashOption(required=False, default=0, description="Index of the play you want to get (Default = 0)")):
        await interaction.response.defer()
        ## Check if user has account binded and if user has specified an UID in the command options
        if uid is None:
            d_id = str(interaction.user.id)
            u_data = mongodb_handler.get_profile(d_id)
            try:
                user_id = u_data.get("uid")
            except Exception:
                await interaction.followup.send("You didn't specify an UID, and you don't have any account binded.")
                return
        else:
            user_id = uid
        ## Calling API for user info
        async with aiohttp.ClientSession() as session:
            api_url = f'{config.domain}/api/recent?id={user_id}&index={index}'
            async with session.get(api_url) as response:
                if response.status == 200:
                    try:
                        data = await response.json()
                    except Exception:
                        await interaction.followup.send("Response is invalid, it may be empty, if account is new, ignore this error.")
                        return
                    ## Parsing the data
                    if isinstance(data, list):
                            item = data[0]
                            # Parsing the data
                            acc = float(item.get("acc", "N/A"))
                            combo = item.get("combo", "N/A")
                            h100 = item.get("hit100", "N/A")
                            h300 = item.get("hit300", "N/A")
                            h50 = item.get("hit50", "N/A")
                            hmiss = item.get("hitmiss", "N/A")
                            hgeki = item.get("hitgeki", "N/A")
                            hkatsu = item.get("hitkatsu", "N/A")
                            h300f = int(h300 + hgeki)
                            h100f = int(h100 + hkatsu)
                            mods = Mods(item.get("mods", "N/A")).convert_std
                            pp = item.get("pp", "N/A")
                            maphash = item.get("maphash", "N/A")
                    
                    osuapi = f"https://osu.ppy.sh/api/get_beatmaps?k={config.osu_key}&h={maphash}"
                    async with session.get(osuapi) as response:
                        if response.status == 200:
                            data = await response.json()
                            ## Parsing map data
                            if isinstance(data, list):
                                for item in data:
                                    artist = item.get("artist", "N/A")
                                    title = item.get("title", "N/A")
                                    version = item.get("version", "N/A")
                                    max_combo = item.get("max_combo")
                                    sr = float(item.get("difficultyrating"))
                                    setid = item.get("beatmapset_id")
                                    diffid = item.get("beatmap_id")

                            ## Sending the embed
                            embed = nextcord.Embed(title=f"☆ {round(sr, 2)} {artist} - {title} [{version}] +{mods}", url=f"https://osu.ppy.sh/beatmapsets/{setid}#osu/{diffid}", color=0x00ff00)
                            embed.set_thumbnail(url=f"https://b.ppy.sh/thumb/{setid}l.jpg")
                            embed.add_field(name="PP:", value=f"{round(pp)}pp")
                            embed.add_field(name="Acc:", value=f"{round(acc, 2)}%")
                            embed.add_field(name="Combo:", value=f"{combo}/{max_combo}x")
                            embed.add_field(name="Judgements:", value=f"300: {h300f}x | 100: {h100f}x | 50: {h50}x | X: {hmiss}x", inline=True)
                            await interaction.followup.send(embed=embed, content=f"Recent play for UID: {user_id} (Index: {index})")
                        else:
                            await interaction.followup.send("Couldn't fetch map data, maybe map isn't submitted on osu! website")
                else:
                    await interaction.followup.send("Couldn't fetch the data.")

def setup(bot):
    if bot.get_cog("recent") is None:
        bot.add_cog(Recent(bot))
