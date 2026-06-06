from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    # "production" en prod, "development" en local
    ENVIRONMENT: str = "development"
    # Domaine de production (ex: predilection.fr)
    DOMAIN_NAME: str = "localhost"

    # Charge le fichier .env automatiquement
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()