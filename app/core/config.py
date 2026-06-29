from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0

    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env", extra="ignore")


# instantiate settings after the class is defined
settings = Settings()