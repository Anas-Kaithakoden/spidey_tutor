from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    gemini_api_key: str = ''
    gemini_model: str = 'gemini-3-flash-preview'
    database_url: str = 'sqlite:///./spidey.db'
    cors_origins: str = '*'


settings = Settings()

