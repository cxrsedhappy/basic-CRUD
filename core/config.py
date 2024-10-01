import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Setting(BaseModel):
    DB_URL: str = os.environ.get('DATABASE_URL')
    DB_ECHO: bool = True
    ALGORITHM: str = os.environ.get('ALGORITHM')
    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7


setting = Setting()
