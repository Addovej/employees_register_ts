from typing import Union

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    PORT: int = 8070
    ENV_NAME: str = 'local'
    DEBUG: bool = True
    LOG_LEVEL: str = 'INFO'
    API_ROOT: str = '/api'
    BACKEND_CORS_ORIGINS: Union[list[AnyHttpUrl], str] = ''

    STATIC_PATH: str = '/frontend'

    POSTGRES_DSN: str
