import os
from typing import Any

from pydantic import BaseSettings, PostgresDsn


class DevConfig(BaseSettings):
    DB_DSN: PostgresDsn
    STREAM_URI: str
    DATABASE: str = "webkpi"
    STREAM_TOPIC: str = "webkpi"
    SCHEDULE_FILE: str = "schedule.csv"
    CA_FILE: str = "./ca.pem"
    CERT_FILE: str = "./service.cert"
    KEY_FILE: str = "./service.key"


class TestConfig(BaseSettings):
    DB_DSN: str = "sqlite://memory"
    STREAM_URI: str = "some"
    DATABASE: str = "webkpi"
    STREAM_TOPIC: str = "webkpi"
    SCHEDULE_FILE: str = "schedule.csv"
    CA_FILE: str = "./ca.pem"
    CERT_FILE: str = "./service.cert"
    KEY_FILE: str = "./service.key"


class ProdConfig(BaseSettings):
    DB_DSN: PostgresDsn
    STREAM_URI: str
    DATABASE: str
    STREAM_TOPIC: str
    SCHEDULE_FILE: str
    CA_FILE: str
    CERT_FILE: str
    KEY_FILE: str


class FactoryConfig:
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if os.getenv("ENVIRONMENT") == "PRODUCTION":
            return ProdConfig()
        elif os.getenv("ENVIRONMENT") == "DEVELOPMENT":
            return DevConfig()
        return TestConfig()
