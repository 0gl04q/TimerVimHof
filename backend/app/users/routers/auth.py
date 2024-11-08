from fastapi import APIRouter, HTTPException, status

from app.users.dao import UserDAO
from app.users.schemas import SUserRegister, SUserAuth
from app.users.auth import authenticate_user
from app.users.utils import create_access_token


router = APIRouter(prefix='/auth', tags=['Авторизация'])


@router.post('/register', summary='Регистрация')
async def register_user(user: SUserRegister) -> dict:
    result = await UserDAO.find_one_or_none(email=user.email)
    if result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пользователь уже существует')
    await UserDAO.add(**user.model_dump())
    return {'message': 'Вы успешно зарегистрировались!'}


@router.post('/login', summary='Вход')
async def auth_user(user_data: SUserAuth):
    check = await authenticate_user(user_data.email, user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверная логин или пароль')
    access_token = create_access_token({'sub': str(check.id)})
    return {'access_token': access_token, 'refresh_token': None}
