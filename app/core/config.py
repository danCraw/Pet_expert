import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv()


class GlobalConfig(BaseSettings):
    DESCRIPTION = "App description"
    DEBUG: bool = False
    TESTING: bool = False
    TIMEZONE: str = "UTC"
    SERVICE_NAME = "PetExpert"
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "DEV")
    API_V1_STR: str = "/api/v1"

    # Database config
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: str = os.environ.get("DB_PORT")
    DB_USER: str = os.environ.get("DB_PORT")
    DB_PASSWORD: str = os.environ.get("DB_PORT")
    DATABASE_URL: Optional[PostgresDsn] = os.environ.get(
        "DATABASE_URL",
        "postgresql+asyncpg://" + DB_USER + ":" + "DB_PASSWORD" + "@" + "DB_HOST" + ":" + "DB_PORT" + "/" + "DB_NAME"
    )
    DB_MIN_SIZE: int = 2
    DB_MAX_SIZE: int = 15
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):
    DESCRIPTION = "Dev web description"
    DEBUG = True


class TestConfig(GlobalConfig):
    DESCRIPTION = "Dev web description"
    DEBUG = True
    TESTING = True
    DB_FORCE_ROLL_BACK = True


class FactoryConfig:
    """Returns a config instance depends on the ENV_STATE variable."""

    def __init__(self, environment: Optional[str] = "DEV"):
        self.environment = environment

    def __call__(self):
        if self.environment == "TEST":
            return TestConfig()
        return DevConfig()


def get_configuration():
    return FactoryConfig(GlobalConfig().ENVIRONMENT)()


config = get_configuration()
