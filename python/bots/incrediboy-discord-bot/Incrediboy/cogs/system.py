import os

from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID", "0"))
class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shutdown", description="Apaga el bot (solo administradores)")
    async def shutdown(self, interaction):
        if interaction.user.id != BOT_OWNER_ID: # Tu ID
            await interaction.response.send_message("❌ No tienes permiso para apagarme.", ephemeral=True)
            return
        await interaction.response.send_message("⚡ Apagando Incrediboy...")
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(System(bot))
