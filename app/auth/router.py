import random
from app.database import get_db
from passlib.hash import bcrypt
from sqlmodel import Session, select
from httpx._client import AsyncClient
from datetime import datetime, timedelta
from .models import AuthToken, UserForm, User, Otp
from fastapi.security import OAuth2PasswordRequestForm as OA2Form
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from .config import gen_token, FAST2SMS_API_KEY, OTP_EXPIRE_MINUTES

auth_routes = APIRouter(prefix='/auth')


@auth_routes.post('/token', response_model=AuthToken)
def token(form: OA2Form = Depends(), db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.phone == form.username)).first()
    if user and bcrypt.verify(form.password, user.password):
        return {'access_token': gen_token(user.dict())}
    raise HTTPException(status_code=401, detail="User not found!")


@auth_routes.post('/signup', response_model=AuthToken)
def signup(form: UserForm = Body(), db: Session = Depends(get_db)):
    otp = db.exec(select(Otp).where(Otp.phone == form.phone)).first()
    if not otp:
        raise HTTPException(status_code=401, detail='Otp not not found!')
    if otp.exp < datetime.now():
        raise HTTPException(status_code=403, detail='Opt expired!')
    if not bcrypt.verify(form.otp, otp.otp):
        raise HTTPException(status_code=401, detail='Wrong otp!')

    user = db.exec(select(User).where(User.phone == form.phone)).first()
    if user:
        return {'access_token': gen_token(user.dict())}

    user = User(phone=form.phone, password=bcrypt.encrypt(form.password))
    db.add(user), db.commit()  # ✓ Registation Complate;
    return {'access_token': gen_token(user.dict())}


@auth_routes.post('/register')
async def register(phone: str = Query(regex='^[0-9]{10}$'), db: Session = Depends(get_db)):
    otp = db.exec(select(Otp).where(Otp.phone == phone)).first()
    if otp and otp.exp > datetime.now():
        raise HTTPException(
            status_code=403, detail='1 OTP/min, Please wait & retry!')

    otp = Otp() if not otp else otp
    _otp = str(random.randint(1000, 9999))
    otp.phone, otp.otp = phone, bcrypt.hash(_otp)
    otp.exp = datetime.now() + timedelta(minutes=OTP_EXPIRE_MINUTES)
    db.add(otp), db.commit()  # Otp Generated!
    async with AsyncClient() as client:
        url = "https://www.fast2sms.com/dev/bulkV2?authorization=" + \
            FAST2SMS_API_KEY + \
            f"&variables_values={_otp}&route=otp&numbers={phone}"
        await client.get(url, headers={'Content-Type': 'application/json'})
    return 'otp sent successfully'
