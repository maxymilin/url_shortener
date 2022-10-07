from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    user_name: str = "user"
    password: str = "password"
    host: str = "localhost"
    db_name: str = "shortener_url"
    db_url: str = f"mysql+asyncmy://{user_name}:{password}@{host}/{db_name}"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
