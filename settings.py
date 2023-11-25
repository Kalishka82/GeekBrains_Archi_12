from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    TEST_DATABASE_URL: str
    DATABASE_URL: str

    class Config:
        env_file = '.env'


settings = Settings()
