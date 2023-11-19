# Neko Cookie bot

Бот амдіністратор для телерам чату

----

Приклад запуску через докер

```sh
docker run --rm -d \
-e BOT_TOKEN=ttt \
-e BOT_ADMIN_CHAT=60123432 \
-e export BOT_ADMINS=60123432,605432142 \
-e DB_URL=sqlite+aiosqlite:///sqlite.db \
--mount type=bind,source=./sqlite.db,target=/project/sqlite.db \
neko_bot
```
