import os
import jwt
from typing import Optional
from sqlmodel import Session
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone as tz, timedelta as tdelta


JWT_ALGORITHM = "HS256"
OTP_EXPIRE_MINUTES = 1
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12
OA2Token = OAuth2PasswordBearer(tokenUrl='auth/token')
JWT_SECRAT_KEY = os.getenv('JWT_SECRAT_KEY', 'd32y78dN')
FAST2SMS_API_KEY = os.getenv('FAST2SMS_API_KEY', 'xxxxxxxxx')


def gen_token(payload: dict, key=JWT_SECRAT_KEY):
    payload['exp'] = datetime.now(tz=tz.utc)  # Current Time;
    payload['exp'] += tdelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, key, JWT_ALGORITHM)


def parse_token(token: str, db: Optional[Session] = None):
    try:
        usr = jwt.decode(token, JWT_SECRAT_KEY, JWT_ALGORITHM)
        if not db:
            return usr
        # TODO: Validate user from Database;
        raise HTTPException(status_code=401, detail='Not yet implimented!')

    except:
        raise HTTPException(status_code=401, detail='Invalid access token!')
