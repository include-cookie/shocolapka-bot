from aiogram import Dispatcher

from app.handlers import (
    base,
    dialog,
    join_request,
    restrictions,
)

def register(dp: Dispatcher):
    dp.include_router(restrictions.router)
    dp.include_router(join_request.router)
    dp.include_router(dialog.router)
    dp.include_router(base.router)
