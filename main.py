import nextcord
from nextcord.ext import commands
import os
import config

bot = commands.Bot()


@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
    ## Loads commands and changes activity
    load_extensions()
    await bot.sync_all_application_commands()
    await bot.change_presence(
        status=nextcord.Status.online,
        activity=nextcord.Activity(
            type=nextcord.ActivityType.listening, name="Harumachi Clover"
        ),
    )


## Command Handler
def load_extensions():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py") and not filename.startswith("__"):
            try:
                bot.load_extension(f"commands.{filename[:-3]}")
                print(f"Loaded extension: {filename}")
            except Exception as e:
                print(f"Failed to load extension {filename}: {e}")


## Logging in...
bot.run(config.discord_token)
