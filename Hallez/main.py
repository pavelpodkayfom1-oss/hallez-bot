import os
import sys
import asyncio
import disnake
from disnake.ext import commands
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from database import init_db
from utils.checks import load_config
from cogs.recruitment import RecruitLaunchView
from cogs.promotions import PromotionLaunchView
from cogs.events import EventAttendanceView

load_dotenv()

intents = disnake.Intents.default()
intents.members = True

guild_id_str = os.getenv("GUILD_ID", "0")
test_guilds = [int(guild_id_str)] if guild_id_str.isdigit() and int(guild_id_str) > 0 else None

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    intents=intents,
    test_guilds=test_guilds,
    reload=True
)

COGS = [
    "cogs.recruitment",
    "cogs.promotions",
    "cogs.admin",
    "cogs.events",
    "cogs.profile",
    "cogs.games",
    "cogs.checkers",
    "cogs.hall_tools",
    "cogs.famq_control"
]

@bot.event
async def on_ready():
    bot.add_view(RecruitLaunchView())
    bot.add_view(PromotionLaunchView())
    bot.add_view(EventAttendanceView())

    try:
        await bot._sync_application_commands()
        print("⚡ Слеш-команды успешно синхронизированы с Discord API!", flush=True)
    except Exception as e:
        print(f"⚠️ Ошибка синхронизации команд: {e}", file=sys.stderr, flush=True)

    config = load_config()
    bot_name = config.get("bot_name", "Hallez FAMQ")
    
    activity = disnake.Activity(
        type=disnake.ActivityType.watching,
        name=f"за порядком в {bot_name} | /admin"
    )
    await bot.change_presence(status=disnake.Status.online, activity=activity)

    print("=" * 60, flush=True)
    print(f"⚜️  Бот {bot_name} успешно запущен!", flush=True)
    print(f"👤  Авторизован как: {bot.user} (ID: {bot.user.id})", flush=True)
    print(f"🌐  Серверов: {len(bot.guilds)} | Задержка: {round(bot.latency * 1000)}ms", flush=True)
    for g in bot.guilds:
        print(f"    • Сервер: {g.name} (ID: {g.id}) | Участников: {g.member_count}", flush=True)
    print(f"📁  Загружено модулей: {len(COGS)}", flush=True)
    print("=" * 60, flush=True)

@bot.event
async def on_slash_command_error(inter: disnake.ApplicationCommandInteraction, error: Exception):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"Ошибка при выполнении команды /{inter.data.name}: {error}", file=sys.stderr, flush=True)
    try:
        if not inter.response.is_done():
            await inter.response.send_message(f"❌ Произошла внутренняя ошибка: `{str(error)}`", ephemeral=True)
        else:
            await inter.followup.send(f"❌ Произошла внутренняя ошибка: `{str(error)}`", ephemeral=True)
    except Exception:
        pass

async def main():
    await init_db()
    
    for cog in COGS:
        try:
            bot.load_extension(cog)
            print(f"✅ Модуль {cog} успешно загружен", flush=True)
        except Exception as e:
            print(f"❌ Ошибка загрузки модуля {cog}: {e}", file=sys.stderr, flush=True)

    token = os.getenv("BOT_TOKEN")
    if not token or token.strip() == "your_bot_token_here":
        print("⚠️  ВНИМАНИЕ: BOT_TOKEN не установлен в файле .env!", flush=True)
        print("👉  Откройте .env и укажите токен вашего бота перед запуском.", flush=True)
        return

    print("🔌 Подключение к Discord Gateway...", flush=True)
    await bot.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен администратором.", flush=True)
