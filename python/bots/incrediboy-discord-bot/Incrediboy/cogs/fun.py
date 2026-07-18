import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
import random
import math
import aiohttp
import datetime
from Incrediboy.utils.helpers import Database


# ───────────────────────────────
# 🧠 Clase principal: Fun (comandos generales)
# ───────────────────────────────
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hola", description="Saluda con estilo 😎")
    async def hola(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"¡Hola {interaction.user.name}! Soy Incrediboy 🤖")

    # 🎱 /8ball
    @app_commands.command(name="8ball", description="Hazle una pregunta a Incrediboy y obtén su sabia respuesta")
    @app_commands.describe(pregunta="Tu pregunta para la bola mágica")
    async def eightball(self, interaction: discord.Interaction, pregunta: str):
        respuestas = [
            "Sí, definitivamente 😎", "No lo creo... 🤔", "Puede ser 👀",
            "¡Claro que sí! 💪", "Mmm... pregúntame más tarde 😴", "No cuentes con eso 😬",
            "Las probabilidades son bajas 😕", "¡Por supuesto que sí! 🌟", "Eso es un rotundo NO 🚫",
            "No estoy seguro... necesito más RAM 💻"
        ]

        def generar_respuesta():
            return random.choice(respuestas)

        class EightBallView(View):
            def __init__(self):
                super().__init__(timeout=30)

            @discord.ui.button(label="🎲 Volver a preguntar", style=discord.ButtonStyle.primary)
            async def volver(self, interaction_boton: discord.Interaction, button: Button):
                nueva_respuesta = generar_respuesta()
                embed = discord.Embed(
                    title="🎱 La bola mágica de Incrediboy",
                    description=f"**{interaction.user.name} pregunta:** {pregunta}\n\n💬 **Nueva respuesta:** {nueva_respuesta}",
                    color=discord.Color.purple()
                ).set_footer(text="Incrediboy nunca se equivoca 😎")
                await interaction_boton.response.edit_message(embed=embed, view=self)

            @discord.ui.button(label="❌ Cerrar", style=discord.ButtonStyle.danger)
            async def cerrar(self, interaction_boton: discord.Interaction, button: Button):
                if interaction_boton.user != interaction.user:
                    return await interaction_boton.response.send_message(
                        "❌ Solo quien hizo la pregunta puede cerrar esto.", ephemeral=True
                    )
                await interaction_boton.response.edit_message(
                    content="🔮 ¡Gracias por consultar a la bola mágica!", embed=None, view=None
                )
                self.stop()

        embed = discord.Embed(
            title="🎱 La bola mágica de Incrediboy",
            description=f"**{interaction.user.name} pregunta:** {pregunta}\n\n💬 **Respuesta:** {generar_respuesta()}",
            color=discord.Color.purple()
        ).set_footer(text="La sabiduría de Incrediboy nunca falla 😎")

        await interaction.response.send_message(embed=embed, view=EightBallView())

    # 🖼️ /pfp
    @app_commands.command(name="pfp", description="Muestra tu foto de perfil en grande")
    @app_commands.describe(user="Usuario del que quieres ver la foto (opcional)")
    async def pfp(self, interaction: discord.Interaction, user: discord.User = None):
        user = user or interaction.user
        embed = (
            discord.Embed(title=f"Foto de perfil de {user.name}", color=discord.Color.blue())
            .set_image(url=user.display_avatar.replace(size=1024, format='png').url)
            .set_footer(text=f"Solicitado por {interaction.user.name}")
        )
        await interaction.response.send_message(embed=embed)


# ───────────────────────────────
# 🎰 Slots & Economía
# ───────────────────────────────
class Slots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    def format_time(self, seconds: int):
        """Convierte segundos a formato h:m:s legible."""
        hours = math.floor(seconds / 3600)
        minutes = math.floor((seconds % 3600) / 60)
        seconds = math.floor(seconds % 60)
        return f"{hours}h {minutes}m {seconds}s"

    @app_commands.command(name="slot", description="🎰 Juega a las tragamonedas apostando una cantidad de monedas.")
    @app_commands.describe(cantidad="Cantidad de monedas a apostar (mínimo 10)")
    async def slot(self, interaction: discord.Interaction, cantidad: int):
        user_id = interaction.user.id
        balance = self.db.get_user_balance(user_id)

        if cantidad < 10:
            return await interaction.response.send_message("⚠️ Apuesta mínima: **10 monedas**.", ephemeral=True)
        if balance < cantidad:
            return await interaction.response.send_message(
                f"❌ No tienes saldo suficiente. Tu saldo actual es {balance} monedas.", ephemeral=True
            )

        emojis = ["🍒", "🍋", "🍇", "🍉", "⭐", "💎"]
        slots = [random.choice(emojis) for _ in range(3)]
        self.db.update_balance(user_id, -cantidad)

        # Evaluación del resultado
        combinaciones = len(set(slots))
        multiplicador = {1: 6, 2: 2}.get(combinaciones, 0)
        ganancia = cantidad * multiplicador if multiplicador else 0

        if ganancia > 0:
            self.db.update_balance(user_id, ganancia)

        result_text = {
            1: f"🎉 **JACKPOT!** Ganaste {ganancia} monedas! (x6)",
            2: f"✨ Dos iguales, ganaste {ganancia} monedas! (x2)",
            3: "😢 No ganaste esta vez."
        }[combinaciones]

        color = {1: discord.Color.gold(), 2: discord.Color.green(), 3: discord.Color.red()}[combinaciones]
        new_balance = self.db.get_user_balance(user_id)

        embed = discord.Embed(
            title="🎰 Tragamonedas",
            description=f"| {' | '.join(slots)} |\n\n{result_text}",
            color=color
        ).set_footer(text=f"Saldo actual: {new_balance} monedas")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="balance", description="💰 Muestra tu saldo actual.")
    async def balance(self, interaction: discord.Interaction):
        balance = self.db.get_user_balance(interaction.user.id)
        await interaction.response.send_message(f"💰 {interaction.user.mention}, tienes **{balance} monedas**.")

    @app_commands.command(name="topslots", description="🏆 Muestra el ranking de jugadores más ricos.")
    async def topslots(self, interaction: discord.Interaction):
        top = self.db.get_top_users()
        if not top:
            return await interaction.response.send_message("No hay jugadores aún.")

        description = "\n".join(
            f"**#{i}** {self.bot.get_user(uid) or f'Usuario {uid}'} — 💰 {bal}"
            for i, (uid, bal) in enumerate(top, start=1)
        )
        embed = discord.Embed(
            title="🏆 Ranking Tragamonedas",
            description=description,
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="daily", description="🎁 Reclama tu recompensa diaria (cada 24 horas).")
    async def daily(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        can_claim, remaining = self.db.can_claim_daily(user_id)

        if not can_claim:
            return await interaction.response.send_message(
                f"🕐 Ya reclamaste tu daily. Vuelve en **{self.format_time(remaining)}**.",
                ephemeral=True
            )

        reward = 200
        self.db.update_balance(user_id, reward)
        self.db.set_last_daily(user_id)
        new_balance = self.db.get_user_balance(user_id)

        embed = discord.Embed(
            title="🎁 Recompensa diaria",
            description=f"Has recibido **{reward} monedas** 💰\nTu nuevo saldo es **{new_balance} monedas**.",
            color=discord.Color.blurple()
        ).set_footer(text="Puedes volver a reclamar en 24 horas.")
        await interaction.response.send_message(embed=embed)


# ───────────────────────────────
# 😂 Fun Extras
# ───────────────────────────────
class FunExtras(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @app_commands.command(name="profile", description="👤 Muestra tu perfil de jugador.")
    async def profile(self, interaction: discord.Interaction):
        user = interaction.user
        balance = self.db.get_user_balance(user.id)

        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT last_daily FROM users WHERE user_id = ?", (user.id,))
        result = cursor.fetchone()
        conn.close()

        last_daily = result[0] if result else 0
        last_daily_str = (
            datetime.datetime.fromtimestamp(last_daily).strftime("%d/%m/%Y %H:%M:%S")
            if last_daily > 0
            else "Nunca 😢"
        )

        embed = (
            discord.Embed(
                title=f"👤 Perfil de {user.name}",
                color=discord.Color.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            .set_thumbnail(url=user.display_avatar.url)
            .add_field(name="💰 Saldo", value=f"**{balance} monedas**", inline=True)
            .add_field(name="🎁 Último Daily", value=last_daily_str, inline=True)
            .set_footer(text="Sistema de economía Incrediboy")
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="meme", description="😂 Muestra un meme aleatorio de Reddit.")
    async def meme(self, interaction: discord.Interaction):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme") as resp:
                if resp.status != 200:
                    return await interaction.followup.send("❌ No pude obtener un meme ahora.")
                data = await resp.json()

        embed = (
            discord.Embed(
                title=data.get("title", "Meme"),
                url=data.get("postLink", ""),
                color=discord.Color.random()
            )
            .set_image(url=data.get("url"))
            .set_footer(text=f"r/{data.get('subreddit', 'desconocido')} • 😄")
        )
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="say", description="🗣️ El bot repite lo que digas.")
    @app_commands.describe(mensaje="El mensaje que quieres que el bot diga.")
    async def say(self, interaction: discord.Interaction, mensaje: str):
        await interaction.response.send_message("✅ Mensaje enviado.", ephemeral=True)
        embed = discord.Embed(description=mensaje, color=discord.Color.green()).set_footer(
            text=f"🗣️ Pedido por {interaction.user.name}"
        )
        await interaction.channel.send(embed=embed)


# ───────────────────────────────
# 🔧 Setup (solo uno)
# ───────────────────────────────
async def setup(bot):
    await bot.add_cog(Fun(bot))
    await bot.add_cog(Slots(bot))
    await bot.add_cog(FunExtras(bot))
