
from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    SQLALCHEMY_DATABASE_URL: str = ""


setting = Settings()