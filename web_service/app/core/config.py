from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from app.core.db_config import DatabaseConfig

load_dotenv()

class Config(BaseSettings):
    APP_NAME: str = "Web Service"
    PROJECT_NAME: str = "Python Alpha"
    PROJECT_DESC: str = "Python Reference project"
    # service
    SERVICE_NAME: str = "SkillStack_Web_Service"
    SERVICE_DESC: str = "Multi Tenant Web Service"

    PRODUCTION: str = "production"
    DEVELOPMENT: str = "development"
    ENVIRONMENT: str = PRODUCTION

    # Logging Configuration
    LOG_FOLDER: str = "logs"
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE_PATH: str = f"logs/{SERVICE_NAME}.log"

    db_settings: DatabaseConfig = DatabaseConfig()
    if ENVIRONMENT == "development":
        db_settings.DB_SQL_LOGGING = True
    else:
        # for all other logging should be filtered, hence by default false
        db_settings.DB_SQL_LOGGING = False

    # set the db settings to be able to connect to local postgresql db
    # host 127.0.0.1, user: appuser, pw: apppass, db: kbase_dev_db


config = Config()
