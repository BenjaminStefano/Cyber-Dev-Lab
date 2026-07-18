import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View
import datetime

# ───────────────────────────────
# 🧭 PANEL INTERACTIVO /HELP
# ───────────────────────────────
class HelpPanel(View):
    def __init__(self, bot, author: discord.User):
        super().__init__(timeout=180)
        self.bot = bot
        self.author = author

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Evita que otros usuarios usen el panel."""
        if interaction.user != self.author:
            await interaction.response.send_message(
                "❌ Solo quien ejecutó el comando puede usar este panel.", ephemeral=True
            )
            return False
        return True

    @staticmethod
    def base_embed(title: str, description: str, color: discord.Color) -> discord.Embed:
        """Crea el estilo base para todos los embeds."""
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text="Incrediboy • Tu bot de diversión y estilo 🤖")
        return embed

    async def update_embed(self, interaction: discord.Interaction, embed: discord.Embed):
        await interaction.response.edit_message(embed=embed, view=self)

    # 🎮 FUN
    @discord.ui.button(label="Fun", emoji="🎮", style=discord.ButtonStyle.blurple)
    async def fun(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.base_embed("🎮 Comandos de Diversión", "Haz reír a todos con estos comandos:", discord.Color.blurple())
        embed.add_field(name="/hola", value="Saluda con estilo 😎", inline=False)
        embed.add_field(name="/8ball", value="Hazle una pregunta a la bola mágica 🎱", inline=False)
        embed.add_field(name="/pfp", value="Muestra la foto de perfil de un usuario 🖼️", inline=False)
        embed.add_field(name="/say", value="Haz que el bot repita tu mensaje 🗣️", inline=False)
        embed.add_field(name="/meme", value="Muestra un meme aleatorio de Reddit 😂", inline=False)
        await self.update_embed(interaction, embed)

    # 🎰 SLOTS
    @discord.ui.button(label="Slots", emoji="🎰", style=discord.ButtonStyle.green)
    async def slots(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.base_embed("🎰 Tragamonedas y Economía", "Comandos para ganar o perder monedas 💸", discord.Color.green())
        embed.add_field(name="/slot", value="Juega a las tragamonedas 🎰", inline=False)
        embed.add_field(name="/balance", value="Muestra tu saldo actual 💵", inline=False)
        embed.add_field(name="/daily", value="Reclama tu recompensa diaria 🎁", inline=False)
        embed.add_field(name="/topslots", value="Muestra el ranking de jugadores 🏆", inline=False)
        embed.add_field(name="/profile", value="Muestra tu perfil y estadísticas 👤", inline=False)
        await self.update_embed(interaction, embed)

    # ⚙️ INFO
    @discord.ui.button(label="Info", emoji="⚙️", style=discord.ButtonStyle.gray)
    async def info(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.base_embed("⚙️ Información y Utilidad", "Comandos de información general:", discord.Color.dark_gray())
        embed.add_field(name="/help", value="Muestra este panel interactivo 📘", inline=False)
        await self.update_embed(interaction, embed)

    # ❌ CERRAR
    @discord.ui.button(label="Cerrar", emoji="❌", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content="📘 Menú de ayuda cerrado. ¡Nos vemos pronto! 🤖",
            embed=None,
            view=None
        )
        self.stop()


# ───────────────────────────────
# 📘 COMANDO /HELP PRINCIPAL
# ───────────────────────────────
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="📘 Muestra el panel interactivo de ayuda.")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📘 Menú de ayuda de Incrediboy",
            description=(
                "Bienvenido al panel de ayuda interactivo de **Incrediboy** 💫\n\n"
                "Usa los **botones de abajo** para navegar entre las categorías.\n"
                "Solo tú puedes interactuar con este menú."
            ),
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text="Incrediboy • Diversión y estilo en un solo bot 🤖")

        view = HelpPanel(self.bot, interaction.user)
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Help(bot))
