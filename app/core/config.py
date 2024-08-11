import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, EmailStr


class Constant:
    LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
    DT_FORMAT = '%d.%m.%Y %H:%M:%S'
    BASE_DIR = Path(__file__).parent
    # Эквивалентно 1 мегабайту(1 MB), 10 ** 6 равно 1 000 000.
    MAX_BYTES = 10 ** 6 / 10 ** 6
    BACKUP_COUNT = 5  # Number of backups
    NAME_FLD_MIN_LEN = 1
    NAME_FLD_MAX_LEN = 100


def configure_logging():
    log_dir = Constant.BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'user.log'

    rotating_handler = RotatingFileHandler(
        log_file,
        maxBytes=Constant.MAX_BYTES,
        backupCount=Constant.BACKUP_COUNT
    )
    logging.basicConfig(
        datefmt=Constant.DT_FORMAT,
        format=Constant.LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )


class Settings(BaseSettings):
    app_title: str = 'Кошачий благотворительный фонд'
    app_description: str = 'Сервис для поддержки котиков!'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    jwt_token_lifetime: int = 3600
    user_password_min_len: int = 3
    # Переменные для Google API
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
