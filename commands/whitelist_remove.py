import nextcord
from nextcord.ext import commands
import aiohttp
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
        async with aiohttp.ClientSession() as session:
            api_url = (
                f"https://osu.ppy.sh/api/get_beatmaps?k={config.osu_key}&s={setid}"
            )
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    beatmap_ids = [
                        item["beatmap_id"] for item in data if "beatmap_id" in item
                    ]

                    # Collect data from the second API for each ID
                    collected_data = []
                    for beatmap_id in beatmap_ids:
                        ## Inserting maps into whitelist
                        second_api_url = f"{config.domain}/api/wl_remove?key={config.wl_key}&bid={beatmap_id}"
                        async with session.get(second_api_url) as second_response:
                            if second_response.status == 200:
                                pass
                            else:
                                collected_data.append(
                                    {"id": id, "error": "Failed to fetch details"}
                                )

                    await interaction.followup.send("Done.")
                else:
                    await interaction.followup.send(
                        "Failed to fetch IDs from the first API."
                    )


def setup(bot):
    if bot.get_cog("WhitelistRemove") is None:
        bot.add_cog(WhitelistRemove(bot))
