from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    algorithm: str
    secret_key: str
    access_token_expire: str
    refresh_token_expire: str

    model_config = SettingsConfigDict(env_file = ".env")

settings = Settings()