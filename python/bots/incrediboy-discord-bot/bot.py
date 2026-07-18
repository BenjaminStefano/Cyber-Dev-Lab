import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# ───────────────────────────────
# ⚙️ Configuración básica
# ───────────────────────────────
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "No se encontró DISCORD_TOKEN. "
        "Crea un archivo .env usando .env.example como referencia."
    )

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ───────────────────────────────
# 🔄 Cargar todos los COGS automáticamente
# ───────────────────────────────
async def load_cogs():
    cogs_path = "./Incrediboy/cogs"
    if not os.path.exists(cogs_path):
        print(f"❌ No se encontró la carpeta: {cogs_path}")
        return

    for filename in os.listdir(cogs_path):
        if filename.endswith(".py"):
            cog_name = f"Incrediboy.cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"✅ Cargado: {cog_name}")
            except Exception as e:
                print(f"❌ Error al cargar {cog_name}: {e}")

# ───────────────────────────────
# 🤖 Evento al iniciar el bot
# ───────────────────────────────
@bot.event
async def on_ready():
    print(f"🤖 Bot iniciado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 {len(synced)} comandos slash sincronizados correctamente.")
    except Exception as e:
        print(f"⚠️ Error al sincronizar comandos: {e}")

# ───────────────────────────────
# 🚀 Ejecución principal
# ───────────────────────────────
async def main():
    await load_cogs()  # 🔹 Primero cargamos los COGS
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot detenido manualmente.")
