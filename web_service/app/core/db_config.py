from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseConfig(BaseSettings):
    """Encapsulates all database connection definitions and pool settings."""
    DB_USER: str = Field(default="root", env="DB_USER")
    DB_PASSWORD: str = Field(default="root", env="DB_PASSWORD")
    DB_SERVER: str = Field(default="localhost", env="DB_SERVER")
    DB_PORT: int = Field(default=3306, ge=1)
    DB_NAME: str = Field(default="skillstack", env="DB_NAME")
    # PostgreSQL
    DB_DRIVER: str = Field(default="psycopg2", env="DB_DRIVER")

    # Connection Pool Management
    DB_POOL_SIZE: int = Field(default=5, ge=1)
    DB_MAX_OVERFLOW: int = Field(default=10, ge=0)
    DB_POOL_RECYCLE: int = Field(default=1800, ge=-1)
    DB_POOL_PRE_PING: bool = Field(default=True)


    # Wait for a free pooled connection	- 3–5 seconds
    DB_POOL_TIMEOUT: float = Field(default=5.0)

    # Establish a new database connection -	5–10 seconds
    DB_CONNECT_TIMEOUT: float = Field(default=5.0)

    # Bound query execution time - Workload-specific
    DB_QUERY_TIMEOUT: float = Field(default=1.0)

    # Database-side statement execution limit, if supported	- Workload-specific
    DB_STATEMENT_TIMEOUT: float = Field(default=1.0)

    # Need to avoid sensitive SQL parameter logging
    DB_ECHO_SQL_LOGGING: bool = Field(default=False)


    # Allow passing an explicit URL, fallback to None to trigger the validator
    DB_URL: str | None = None

    @model_validator(mode="after")
    def assemble_async_connection(self) -> "DatabaseConfig":
        """ Assemble the connection string using verified fields """
        # If a URL was explicitly passed in the environment, keep it
        if self.DB_URL:
            return self

        # Safely assemble the connection string using verified fields
        self.DB_URL = (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}"
        )
        return self

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Instantiating this will read from environment or your .env file
# db_settings = DatabaseConfig()
