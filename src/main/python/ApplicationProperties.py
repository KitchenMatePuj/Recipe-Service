import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ApplicationProperties:
    DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:my-secret-pw@127.0.0.1:3306/recipe_db")
    APP_PORT = int(os.getenv("APP_PORT", 8000))
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
    RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "notification_queue")
