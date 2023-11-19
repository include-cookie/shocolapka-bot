from os import getenv

TOKEN = getenv("BOT_TOKEN")
ADMIN_CHAT = int(getenv("BOT_ADMIN_CHAT"))
DB_URL = getenv("DB_URL",'sqlite+aiosqlite:///sqlite.db')


ADMINS = set(map(int,getenv("BOT_ADMINS").split(',')))
