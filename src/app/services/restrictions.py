from sqlalchemy import select,func

from app.db.models import Warn


async def give_warn(session,user_id,chat_id,reason=None):
    warn = Warn(
        user_id=user_id,
        chat_id=chat_id,
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


async def get_all_warns(session,user_id,chat_id):
    stmt = select(Warn).where(
        Warn.chat_id == chat_id,
        Warn.user_id == user_id,
    )

    warn_list = await session.execute(stmt)
    warn_list = warn_list.scalars()

    return warn_list
