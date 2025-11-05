import datetime
import jwt
from app.config import TOKEN_AUD, TOKEN_ISS, TOKEN_KEY

async def gen_token(id, tg_id, tg_nickname, roles, avatar_href, full_name):
    payload_data = {
        "tg_id": tg_id,
        "nick": tg_nickname,
        "role": roles,
        "avatar_src": avatar_href,
        "name": full_name,
        "sub": id,
        "iss": TOKEN_ISS,
        "aud": TOKEN_AUD,
        "iat": datetime.datetime.now(tz=datetime.timezone.utc),
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=64)
    }

    new_token = jwt.encode(
        payload= payload_data,
        key = TOKEN_KEY, 
        algorithm="HS256",
    )

    return new_token