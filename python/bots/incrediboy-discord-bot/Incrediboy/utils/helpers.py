import sqlite3
import os
import yt_dlp
import discord
import asyncio
import time 


# --- Base de datos ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "user_warnings.db")

def create_user_table():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users_per_guild (
            user_id INTEGER,
            warning_count INTEGER DEFAULT 0,
            guild_id INTEGER,
            PRIMARY KEY (user_id, guild_id)
        )
    """)
    connection.commit()
    connection.close()

def increase_and_get_warnings(user_id: int, guild_id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT warning_count FROM users_per_guild WHERE user_id = ? AND guild_id = ?;", (user_id, guild_id))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO users_per_guild (user_id, warning_count, guild_id) VALUES (?, 1, ?);", (user_id, guild_id))
        count = 1
    else:
        count = result[0] + 1
        cursor.execute("UPDATE users_per_guild SET warning_count = ? WHERE user_id = ? AND guild_id = ?;", (count, user_id, guild_id))
    connection.commit()
    connection.close()
    return count

# Crear tabla al iniciar
create_user_table()

# --- Música ---
ydl_opts = {'format': 'bestaudio', 'quiet': True}
ffmpeg_opts = {
    'options': '-vn',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

queues = {}

async def play_next(bot, ctx, guild_id):
    if guild_id not in queues or not queues[guild_id]:
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            await ctx.channel.send("✅ Cola terminada, saliendo del canal de voz.")
        return

    title, url = queues[guild_id].pop(0)
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']

    source = await discord.FFmpegOpusAudio.from_probe(audio_url, **ffmpeg_opts)

    def after_playing(error):
        fut = asyncio.run_coroutine_threadsafe(play_next(bot, ctx, guild_id), bot.loop)
        try:
            fut.result()
        except Exception as e:
            print(e)

    voice_client.play(source, after=after_playing)
    await ctx.channel.send(f"🎶 Reproduciendo: **{title}**")


# Base de Datos para Tragamonedas con Emojis
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "slots.db")  # <── GUARDA slots.db en Incrediboy/utils

class Database:
    def __init__(self):
        self.create_db()

    def connect(self):
        return sqlite3.connect(DB_PATH)

    def create_db(self):
        """Crea la base de datos y la tabla si no existen."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 1000,
                last_daily REAL DEFAULT 0
            )
        """)

        conn.commit()
        conn.close()

    # ───────────────────────────────
    # FUNCIONES DE ECONOMÍA
    # ───────────────────────────────
    def get_user_balance(self, user_id: int) -> int:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO users (user_id, balance, last_daily) VALUES (?, ?, ?)", (user_id, 1000, 0))
            conn.commit()
            balance = 1000
        else:
            balance = result[0]

        conn.close()
        return balance

    def update_balance(self, user_id: int, amount: int):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()
        conn.close()

    def get_top_users(self, limit: int = 10):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, balance FROM users ORDER BY balance DESC LIMIT ?", (limit,))
        top = cursor.fetchall()
        conn.close()
        return top

    # ───────────────────────────────
    # SISTEMA DE RECOMPENSA DIARIA
    # ───────────────────────────────
    def can_claim_daily(self, user_id: int, cooldown: int = 86400):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT last_daily FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO users (user_id, balance, last_daily) VALUES (?, ?, ?)", (user_id, 1000, 0))
            conn.commit()
            last_daily = 0
        else:
            last_daily = result[0]

        now = time.time()
        can_claim = (now - last_daily) >= cooldown
        remaining = max(0, cooldown - (now - last_daily))
        conn.close()
        return can_claim, remaining

    def set_last_daily(self, user_id: int):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET last_daily = ? WHERE user_id = ?", (time.time(), user_id))
        conn.commit()
        conn.close()