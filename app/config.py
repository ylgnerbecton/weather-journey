from typing import Optional, List, Union
from pydantic import BaseSettings, Field, validator, AnyHttpUrl


class Settings(BaseSettings):
    """Main settings class. The fields of this class are automatically populated from the environment variables or
    their default values when an instance of this class is created."""

    API_ROOT_PATH: Optional[str] = Field(None, env="API_ROOT_PATH")
    DEBUG: bool = Field(default=False)
    USE_FAKE_AUTHORIZATION: bool = Field(default=False)
    ENVIRONMENT_NAME: str = Field(env="ENVIRONMENT_NAME", default="dev")
    DATABASE_URL: Optional[str] = Field(None, env="DATABASE_URL")
    DB_NAME: Optional[str] = Field(None, env="DB_NAME")
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    API_KEY_OPENWEATHERMAP: Optional[str] = Field(
        env="API_KEY_OPENWEATHERMAP", default="1098ea6c9a71f45cc016bc76392dd6c3"
    )

    TWITTER_CONSUMER_KEY: Optional[str] = Field(
        env="TWITTER_CONSUMER_KEY", default="BdddI4PrI3eE5hFW4X5uGYAV6"
    )
    TWITTER_CONSUMER_SECRET: Optional[str] = Field(
        env="TWITTER_CONSUMER_SECRET",
        default="A4NmfJJS5cX6Cr10njYyXZq1ajFFKnzCTzFZGqgpF9RhB5oOrx",
    )
    TWITTER_ACCESS_TOKEN: Optional[str] = Field(
        env="TWITTER_ACCESS_TOKEN",
        default="1678278567833092098-NmUNAPdqDYbwSoorKXkYslwSfWxdxf",
    )
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = Field(
        env="TWITTER_ACCESS_TOKEN_SECRET",
        default="4nhdXFxp56mrr3QItZlQmjRYWGMl7I6eInPcipRsU7Kdt",
    )

    TELEGRAM_BOT_TOKEN: Optional[str] = Field(
        env="TELEGRAM_BOT_TOKEN",
        default="6081400554:AAEDyBaDGoGyva9ZlgEN442o0wb6KA6DVO0",
    )

    class Config:
        env_file = ".env"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[str, List[str]]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("DATABASE_URL", pre=True)
    def assemble_db_url(cls, v: Optional[str], values) -> str:
        if v is None and values.get("ENVIRONMENT_NAME") == "dev":
            return "mongodb://db_weather:27017/local"
        return v

    @validator("DB_NAME", pre=True)
    def assemble_db_name(cls, v: Optional[str], values) -> str:
        if v is None and values.get("ENVIRONMENT_NAME") == "dev":
            return "local"
        return v


settings = Settings()
