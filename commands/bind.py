import nextcord
from nextcord.ext import commands
from handlers.mongodb import mongodb_handler
import aiohttp
import config
import hashlib

def add_slashes(input_string):
    # Add backslashes to escape characters like single and double quotes
    return input_string.replace("'", "\\'").replace('"', '\\"')

def get_md5_hash(input_string):
    # Compute MD5 hash
    return hashlib.md5(input_string.encode("utf-8")).hexdigest()

class Bind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="bind", description="Bind your profile to your Discord account")
    async def _bind(self, interaction: nextcord.Interaction, username:str = nextcord.SlashOption(required=True, description="Your username used to log into the game."), password:str = nextcord.SlashOption(required=True, description="Password used to log into the game.")):
        await interaction.response.defer(ephemeral=True)
        user_id = str(interaction.user.id)

        async with aiohttp.ClientSession() as session:
            api_url = f"{config.domain}/api/login.php"
            gameversion = 3
            salted_pswd = password + "taikotaiko"
            pswd_hash = get_md5_hash(salted_pswd)
            username = username.strip()
            params = {
                "username": username,  # Strip any potential leading/trailing whitespace
                "password": pswd_hash,
                "version": str(gameversion)  # Make sure version is a string "3"
            }
            async with session.post(api_url, data=params) as response:
                if response.status == 200:
                    response = await response.text()
                    response = response.splitlines()
                    if len(response) >= 2:
                        data = response[1].split()
                        if len(data) < 6:
                            print(response + " Failed 2")
                            await interaction.followup.send("Invalid data sent from server.", ephemeral=True)
                            return
                        uid = int(data[0])
                        # Check if the uid is already bound to another user
                        existing_user = mongodb_handler.find_user_by_uid(uid)
                        if existing_user and existing_user["_id"] != user_id:
                            await interaction.followup.send("This UID is already bound to another account.", ephemeral=True)
                            return
                        already_bound = mongodb_handler.get_profile(user_id)
                        if already_bound and already_bound["_id"] == user_id:
                            await interaction.followup.send("You can't rebind your account, tell Owner for unbind.", ephemeral=True)
                            return
                        mongodb_handler.bind_profile(user_id, uid)
                        await interaction.followup.send(f"User account {username} has been bound successfully!", ephemeral=True)
                    else:
                        print(response + " Failed 1")
                        print("1")
                        await interaction.followup.send("Invalid data sent from server.", ephemeral=True)
                        return

        

def setup(bot):
    if bot.get_cog("Bind") is None:
        bot.add_cog(Bind(bot))
