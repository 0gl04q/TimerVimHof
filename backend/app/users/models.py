from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, int_pk, str_unique


class User(Base):
    id: Mapped[int_pk]
    email: Mapped[str_unique]
    username: Mapped[str]
    password: Mapped[str]

    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    extend_existing = True

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, username={self.username})'

    def __repr__(self):
        return str(self)