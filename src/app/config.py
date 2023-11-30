from os import getenv

DEBUG = (getenv("DEBUG","F").lower()=="true")

TOKEN = getenv("BOT_TOKEN")

ADMIN_CHAT = int(getenv("BOT_ADMIN_CHAT"))

DB_URL = getenv("DB_URL")
