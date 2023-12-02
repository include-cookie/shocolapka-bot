from sqlalchemy import select,func
from aiogram.types import ChatPermissions

from app.db.models import Warn


async def give_warn(session,chat_id,user_id,reason=None):
    warn = Warn(
        chat_id=chat_id,
        user_id=user_id,
        reason=reason
    )

    session.add(warn)
    await session.commit()

    stmt = select(func.count()).where(
        Warn.chat_id == chat_id,
        Warn.user_id == user_id,
    )

    cnt = await session.scalar(stmt)

    return cnt


async def get_all_warns(session,chat_id,user_id):
    stmt = select(Warn).where(
        Warn.chat_id == chat_id,
        Warn.user_id == user_id,
    )

    warn_list = await session.execute(stmt)
    warn_list = warn_list.scalars()

    return warn_list


async def give_mute(bot,chat_id,user_id,period):
    await bot.restrict_chat_member(
        chat_id,
        user_id,
        permissions=ChatPermissions(can_send_messages=False),
        until_date=period
    )
