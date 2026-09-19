from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    gemini_api_key: str = ''
    gemini_model: str = 'gemini-3-flash-preview'

    # Groq (OpenAI-compatible cloud provider)
    groq_api_key: str = ''
    groq_model: str = 'openai/gpt-oss-20b'
    groq_model_strong: str = 'openai/gpt-oss-120b'

    # OpenRouter (OpenAI-compatible aggregator; free models supported)
    openrouter_api_key: str = ''
    openrouter_model: str = 'openrouter/free'
    openrouter_free_models: str = ''

    database_url: str = 'sqlite:///./spidey.db'
    cors_origins: str = '*'


settings = Settings()

