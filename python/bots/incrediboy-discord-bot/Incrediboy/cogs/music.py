import discord
from discord.ext import commands
from discord import app_commands
from Incrediboy.utils.helpers import queues, play_next
from yt_dlp import YoutubeDL
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="join", description="Incrediboy se une a tu canal de voz")
    async def join(self, interaction: discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message("❌ Debes estar en un canal de voz.", ephemeral=True)
            return
        channel = interaction.user.voice.channel
        await channel.connect()
        await interaction.response.send_message(f"✅ Me he unido a {channel.name}.")

    @app_commands.command(name="play", description="Reproduce música desde YouTube y agrega a la cola")
    @app_commands.describe(url="Enlace o nombre de la canción")
    async def play(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer()
        if interaction.user.voice is None or interaction.user.voice.channel is None:
            await interaction.followup.send("❌ Debes estar en un canal de voz.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        if guild_id not in queues:
            queues[guild_id] = []

        ydl_opts = {'format': 'bestaudio', 'quiet': True}

        try:
            with YoutubeDL(ydl_opts) as ydl:
                data = ydl.extract_info(f"ytsearch:{url}", download=False)
                if not data or 'entries' not in data or len(data['entries']) == 0:
                    await interaction.followup.send("⚠️ No se encontró ninguna canción.", ephemeral=True)
                    return
                info = data['entries'][0]
                audio_url = info['webpage_url']
                title = info['title']
        except Exception as e:
            await interaction.followup.send(f"❌ Error al buscar la canción: {e}", ephemeral=True)
            return

        queues[guild_id].append((title, audio_url))
        await interaction.followup.send(f"➕ Agregado a la cola: **{title}**")

        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if not voice_client or not voice_client.is_playing():
            await play_next(self.bot, interaction, guild_id)

    @app_commands.command(name="pause", description="Pausa la música actual")
    async def pause(self, interaction: discord.Interaction):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("⏸️ Música pausada.")
        else:
            await interaction.response.send_message("⚠️ No hay música reproduciéndose.", ephemeral=True)

    @app_commands.command(name="resume", description="Reanuda la música pausada")
    async def resume(self, interaction: discord.Interaction):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await interaction.response.send_message("▶️ Música reanudada.")
        else:
            await interaction.response.send_message("⚠️ No hay música pausada.", ephemeral=True)

    @app_commands.command(name="stop", description="Detiene la música y limpia la cola")
    async def stop(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        queues[guild_id] = []
        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("⏹️ Reproducción detenida y cola vaciada.")
        else:
            await interaction.response.send_message("⚠️ No hay música en reproducción.", ephemeral=True)

    @app_commands.command(name="leave", description="Hace que Incrediboy salga del canal de voz")
    async def leave(self, interaction: discord.Interaction):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            await interaction.response.send_message("👋 Me he desconectado del canal.")
        else:
            await interaction.response.send_message("⚠️ No estoy conectado a ningún canal.", ephemeral=True)

    @app_commands.command(name="queue", description="Muestra la cola de canciones")
    async def queue(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        if guild_id not in queues or not queues[guild_id]:
            await interaction.response.send_message("🎵 La cola está vacía.", ephemeral=True)
            return
        queue_list = "\n".join([f"{i+1}. {t[0]}" for i, t in enumerate(queues[guild_id])])
        await interaction.response.send_message(f"📃 Cola de canciones:\n{queue_list}")

    @app_commands.command(name="skip", description="Salta la canción actual")
    async def skip(self, interaction: discord.Interaction):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("⏭️ Canción saltada.")
        else:
            await interaction.response.send_message("⚠️ No hay música reproduciéndose.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Music(bot))
