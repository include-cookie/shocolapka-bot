from os import getenv

DEBUG = (getenv("DEBUG","F").lower()=="true")

TOKEN = getenv("BOT_TOKEN")

ADMIN_CHAT = int(getenv("BOT_ADMIN_CHAT",0))

DB_URL = getenv("DB_URL")

MAIN_SITE_URL = getenv("MAIN_SITE_URL")
RULE_URL = getenv("RULE_URL")

PANDC_CHAT_ID = getenv("PANDC_CHAT_ID")

TOKEN_KEY = getenv("TOKEN_KEY")
TOKEN_AUD = getenv("TOKEN_AUD")
TOKEN_ISS = getenv("TOKEN_ISS")