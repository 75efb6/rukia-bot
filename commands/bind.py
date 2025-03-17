import nextcord
from nextcord.ext import commands
from handlers.mongodb import mongodb_handler
from handlers.apirequests import DroidAPI
import config
import hashlib


def get_md5_hash(input_string):
    ## Compute MD5 hash
    return hashlib.md5(input_string.encode("utf-8")).hexdigest()  # nosec


class Bind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="bind",
        description="Bind your profile to your Discord account",
    )
    async def _bind(
        self,
        interaction: nextcord.Interaction,
        username: str = nextcord.SlashOption(
            required=True, description="Your username used to log into the game."
        ),
        password: str = nextcord.SlashOption(
            required=True, description="Password used to log into the game."
        ),
    ):
        await interaction.response.defer(ephemeral=True)
        user_id = str(interaction.user.id)
        d_uname = interaction.user.display_name
        response = DroidAPI().login(username=username, passwd=password)
        if response is not False:
            ## Check if the uid is already bound to another user
            existing_user = mongodb_handler.find_user_by_uid(response)
            if existing_user and existing_user["_id"] != user_id:
                await interaction.followup.send(
                    "This UID is already bound to another account.",
                    ephemeral=True,
                )
                return
            already_bound = mongodb_handler.get_profile(user_id)
            if already_bound and already_bound["_id"] == user_id:
                await interaction.followup.send(
                    "You can't rebind your account, tell Owner for unbind.",
                    ephemeral=True,
                )
                return
            mongodb_handler.bind_profile(user_id, response, d_uname, username)
            await interaction.followup.send(
                f"User account {username} has been bound successfully!",
                ephemeral=True,
            )
        else:
            await interaction.followup.send("Invalid login", ephemeral=True)


def setup(bot):
    if bot.get_cog("Bind") is None:
        bot.add_cog(Bind(bot))
