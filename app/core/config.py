from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env")


# instantiate settings after the class is defined
settings = Settings()