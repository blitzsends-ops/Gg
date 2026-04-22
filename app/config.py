from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    openai_chat_model: str = "gpt-4.1-mini"
    openai_image_model: str = "gpt-image-1"

    meta_access_token: str
    meta_ad_account_id: str
    meta_page_id: str
    meta_graph_version: str = "v22.0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
