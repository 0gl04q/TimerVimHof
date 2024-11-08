from app.users.utils import verify_password
from app.users.dao import UserDAO


async def authenticate_user(email: str, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if user and verify_password(password, user.password) is True:
        return user
