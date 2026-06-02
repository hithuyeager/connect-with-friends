from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    algorithm: str
    secret_key: str
    access_token_expire: int
    refresh_token_expire: int
    google_client_id: str
    google_client_secret: str
    google_secret_key: str
    database_url_for_raw_sql: str

    model_config = SettingsConfigDict(env_file = ".env")

settings = Settings()