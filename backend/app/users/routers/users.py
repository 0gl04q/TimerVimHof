from fastapi import APIRouter, Depends

from app.users.dao import UserDAO
from app.users.rb import RBUser
from app.users.schemas import SUser
from app.users.dependencies import get_current_user

router = APIRouter(prefix='/users', tags=['Пользователи'], dependencies=(Depends(get_current_user),))


@router.get('/', summary='Получить пользователей', response_model=list[SUser])
async def get_users(request_body: RBUser = Depends()) -> list[SUser]:
    return await UserDAO.find_all(**request_body.to_dict())


@router.get('/{user_id}', summary='Получить пользователя по id')
async def get_user(user_id: int) -> SUser | dict:
    rez = await UserDAO.find_one_or_none(id=user_id)
    if rez is None:
        return {'message': 'Not found'}
    return rez


@router.get("/by_filter/", summary="Получить пользователя по фильтру")
async def get_user_by_filter(request_body: RBUser = Depends()) -> SUser | dict:
    rez = await UserDAO.find_one_or_none(**request_body.to_dict())
    if rez is None:
        return {'message': 'Not found'}
    return rez


@router.get('/profile/', summary='Профиль пользователя')
async def get_me(current_user: SUser = Depends(get_current_user)) -> SUser:
    return current_user
