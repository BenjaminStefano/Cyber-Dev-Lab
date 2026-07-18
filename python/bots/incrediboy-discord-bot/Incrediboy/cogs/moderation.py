import discord
from discord.ext import commands
from discord import app_commands
from Incrediboy.utils.helpers import increase_and_get_warnings
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clean", description="Borra mensajes del canal actual")
    @app_commands.describe(amount="Número de mensajes a eliminar (máx. 1000)")
    @commands.has_permissions(manage_messages=True)
    async def clean(self, interaction: discord.Interaction, amount: int):
        if amount < 1 or amount > 1000:
            await interaction.response.send_message("⚠️ Debes ingresar un número entre 1 y 1000", ephemeral=True)
            return
        await interaction.response.send_message(f"🧹 Eliminando {amount} mensajes...", ephemeral=True)
        await asyncio.sleep(1)
        await interaction.channel.purge(limit=amount)

    @app_commands.command(name="ban", description="Banea a un usuario del servidor")
    @app_commands.describe(member="Miembro a banear", reason="Razón del baneo (opcional)")
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No especificada"):
        if member == interaction.user:
            await interaction.response.send_message("❌ No puedes banearte a ti mismo.", ephemeral=True)
            return
        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"🚫 {member.name} ha sido baneado. Razón: {reason}")
        except Exception as e:
            await interaction.response.send_message(f"❌ Error al banear: {e}", ephemeral=True)

    @app_commands.command(name="mute", description="Silencia a un usuario")
    @app_commands.describe(member="Miembro a silenciar")
    @commands.has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member):
        guild = interaction.guild
        mute_role = discord.utils.get(guild.roles, name="Muted")
        if not mute_role:
            mute_role = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=True)
        await member.add_roles(mute_role)
        await interaction.response.send_message(f"🔇 {member.mention} ha sido silenciado.")

    @app_commands.command(name="warn", description="Advierte a un usuario y guarda el registro en la base de datos")
    @app_commands.describe(member="Miembro a advertir", reason="Razón de la advertencia")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No especificada"):
        warnings = increase_and_get_warnings(member.id, interaction.guild.id)
        await interaction.response.send_message(
            f"⚠️ {member.mention} ha sido advertido.\nRazón: {reason}\nAdvertencias totales: {warnings}"
        )

async def setup(bot):
    await bot.add_cog(Moderation(bot))
