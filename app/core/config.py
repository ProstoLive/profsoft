from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    API_URL: str
    RESULT_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
