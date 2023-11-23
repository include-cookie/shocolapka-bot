# Neko Cookie bot

Бот адміністратор для телеграм чату

----

Приклад запуску через докер

```sh
docker run --rm -d \
--name neko_bot \
-e DEBUG=False \
-e BOT_TOKEN=tg_token \
-e BOT_ADMIN_CHAT=60123432 \
-e BOT_ADMINS=60123432,605432142 \
-e DB_URL=sqlite+aiosqlite:///db/sqlite.db \
-v ./db:/project/db \
ghcr.io/nitekot/neko_bot:main
```

Перегляд логів за минулу годину

```sh
docker logs -t --since 1h neko_bot
```
