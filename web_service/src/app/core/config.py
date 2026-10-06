
class Settings():
    PROJECT_NAME: str = "Web Service"
    PROJECT_DESC: str = "Web Service"
    # service
    SERVICE_NAME: str = "mt_web_service"

    # Logging Configuration
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE_PATH: str = f"logs/{SERVICE_NAME}.log"

settings = Settings()
