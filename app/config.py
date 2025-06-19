from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_uri: str = "32r89u89ef9w8fe"
    secret_key: str = "your_secret_key"
    algorithm: str  = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()