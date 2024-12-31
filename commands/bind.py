import nextcord
from nextcord.ext import commands
from handlers.mongodb import mongodb_handler

class Bind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="bind", description="Bind your profile to your Discord account")
    async def _bind(self, interaction: nextcord.Interaction, uid: str):
        user_id = str(interaction.user.id)

        # Check if the uid is already bound to another user
        existing_user = mongodb_handler.find_user_by_uid(uid)
        if existing_user and existing_user["_id"] != user_id:
            await interaction.response.send_message("This UID is already bound to another account.", ephemeral=True)
            return

        mongodb_handler.bind_profile(user_id, uid)
        await interaction.response.send_message(f"Profile for {interaction.user.name} has been bound successfully!")

def setup(bot):
    if bot.get_cog("Bind") is None:
        bot.add_cog(Bind(bot))
