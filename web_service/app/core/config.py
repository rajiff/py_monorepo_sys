from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    APP_NAME: str = "Web Service"
    PROJECT_NAME: str = "Python Alpha"
    PROJECT_DESC: str = "Python Reference project"
    # service
    SERVICE_NAME: str = "mt_web_service"
    SERVICE_DESC: str = "Multi Tenant Web Service"

    # Logging Configuration
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE_PATH: str = f"logs/{SERVICE_NAME}.log"

config = Config()
