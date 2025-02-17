"""
Configuration Settings for the Application.

This module defines the `Settings` class, which is used to manage configuration settings
for the application using Pydantic's `BaseSettings`. It includes settings for the application
mode, database, Redis, SMTP server, and other external services.

The settings are loaded from environment variables (via a `.env` file), and the class provides
properties for generating database URLs for both production and testing environments.
"""

from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    A class that holds the application's configuration settings.

    This class uses Pydantic's `BaseSettings` to load configuration values from environment
    variables, with a `.env` file for development and testing purposes. It includes properties
    for database URLs, SMTP configuration, Redis, and other external services
    required by the application.

    Attributes:
        MODE (Literal["DEV", "PROD", "TEST"]): The environment mode of the application.
        LOG_LEVEL (Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]): The logging level.
        DATABASE_URL (str): The URL for connecting to the production database.
        TEST_DATABASE_URL (str): The URL for connecting to the test database.
        SMTP configuration variables: For sending emails through SMTP.
        REDIS configuration variables: For connecting to Redis for caching.
        SECRET_KEY_FOR_HASH (str): The secret key used for hashing tokens and passwords.
        ALGORITHM_FOR_HASH (str): The algorithm used for hashing tokens and passwords.
        SENTRY_LINK (str): The Sentry link for error tracking.
    """

    MODE: Literal["DEV", "PROD", "TEST"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    SECRET_KEY_FOR_HASH: str
    ALGORITHM_FOR_HASH: str
    SENTRY_LINK: str

    @property
    def DATABASE_URL(self) -> str:
        """
        Generates the database URL for connecting to the PostgreSQL database.

        Returns:
            str: The PostgreSQL database connection string.
        """
        db_creds = f'{self.DB_USER}:{self.DB_PASS}'
        db_address = f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        return f"postgresql+asyncpg://{db_creds}@{db_address}"

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    TEST_SMTP_HOST: str
    TEST_SMTP_PORT: int
    TEST_SMTP_USER: str
    TEST_SMTP_PASS: str

    TEST_REDIS_HOST: str
    TEST_REDIS_PORT: int

    @property
    def TEST_DATABASE_URL(self) -> str:
        """
        Generates the database URL for connecting to the test PostgreSQL database.

        Returns:
           str: The PostgreSQL test database connection string.
        """
        test_db_creds = f'{self.TEST_DB_USER}:{self.TEST_DB_PASS}'
        test_db_address = f'{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}'
        return f"postgresql+asyncpg://{test_db_creds}@{test_db_address}"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
