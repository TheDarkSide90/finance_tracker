from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Finance Tracker'
    database_url: str | None = None
    secret: str = 'SECRET'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
