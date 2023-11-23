from os import getenv

DEBUG = bool(getenv("DEBUG",False))

TOKEN = getenv("BOT_TOKEN")

ADMIN_CHAT = int(getenv("BOT_ADMIN_CHAT"))
ADMINS = set(map(int,getenv("BOT_ADMINS").split(',')))

DB_URL = getenv("DB_URL",'sqlite+aiosqlite:///sqlite.db')
