# Neko Cookie bot

Бот адміністратор для телеграм чату

----

Приклад запуску через докер

```sh
docker run --rm -d \
-e DEBUG=False \
-e BOT_TOKEN=tg_token \
-e BOT_ADMIN_CHAT=60123432 \
-e BOT_ADMINS=60123432,605432142 \
-e DB_URL=sqlite+aiosqlite:///db/sqlite.db \
-v ./db:/project/db \
ghcr.io/nitekot/neko_bot:latest
```
