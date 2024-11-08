from app.dao import BaseDAO
from app.users.models import User
from app.users.utils import hash_password


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add(cls, **values):
        values['password'] = hash_password(values['password'])
        return await super().add(**values)

