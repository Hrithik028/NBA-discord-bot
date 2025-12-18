import discord
from discord.ext import commands
from config import DISCORD_TOKEN, COMMAND_PREFIX

from commands.nba_cmd import setup_nba_commands
from commands.scoreboard_cmd import setup_scoreboard_commands
from commands.player_cmd import setup_player_commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# Register commands
setup_nba_commands(bot)
setup_scoreboard_commands(bot)
setup_player_commands(bot)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Static token (no env vars)
bot.run(DISCORD_TOKEN)
