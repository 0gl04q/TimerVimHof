from pydantic_settings import BaseSettings
from passlib.context import CryptContext


class Settings(BaseSettings):
    DB_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    PWD_CONTEXT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    BOT_TOKEN: str
    BASE_SITE: str
    ADMIN_ID: str


settings = Settings()


def get_db_url() -> str:
    return (f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
            f"@{settings.DB_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")


def get_webhook_url() -> str:
    return f"{settings.BASE_SITE}/webhook"
