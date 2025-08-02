from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


env_path = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    def db_url_psycopg(self):
        # postgresql+psycopg://postgres:postgres@localhost:5432/pizzadb
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def db_url_asyncpg(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/pizzadb
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=env_path)


settings = Settings()
