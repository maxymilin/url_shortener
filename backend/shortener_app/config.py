from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    env_name: str = "Local"
    user_name: str = "root"
    password: str = "root"
    host: str = "mysqldb"
    port: str = "3306"
    db_name: str = "shortener_url"
    db_url: str = f"mysql+asyncmy://{user_name}:{password}@{host}:{port}/{db_name}"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
