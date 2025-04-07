from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from src import config
from common.alerts import (
    AlertsProcessor,
    MattermostProcessor,
    SlackProcessor,
    DefaultProcessor,
)


class DBConfig(BaseModel):
    DRIVER: str = Field(default=config.DB_CONFIG["DRIVER"])
    HOST: str = Field(default=config.DB_CONFIG["HOST"])
    PORT: int = Field(default=config.DB_CONFIG["PORT"])
    USER: str = Field(default=config.DB_CONFIG["USER"])
    PASSWORD: str = Field(default=config.DB_CONFIG["PASSWORD"])
    NAME: str = Field(default=config.DB_CONFIG["NAME"])


class AlertsProcessorConfig(BaseModel):
    type: str = Field(default=config.ALERTS_PROCESSOR["type"])
    url: str = Field(default=config.ALERTS_PROCESSOR["url"])
    channel: str | None = Field(default=config.ALERTS_PROCESSOR.get("channel"))


class S3Config(BaseModel):
    REGION_NAME: str = Field(default=config.AWS_S3["REGION_NAME"])
    BUCKET_NAME: str = Field(default=config.AWS_S3["BUCKET_NAME"])


def setup_alert_process(alerts_config: AlertsProcessorConfig) -> AlertsProcessor:
    if alerts_config.type == "Mattermost":
        return MattermostProcessor(alerts_config.url)
    elif alerts_config.type == "Slack":
        return SlackProcessor(url=alerts_config.url, channel=alerts_config.channel)
    else:
        return DefaultProcessor()


class Settings(BaseSettings):
    db: DBConfig = Field(default_factory=DBConfig)
    alerts_processor: AlertsProcessorConfig = Field(default_factory=AlertsProcessorConfig)
    aws_s3: S3Config = Field(default_factory=S3Config)

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")


settings = Settings()
