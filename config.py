import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "postgresql+asyncpg://username:password@localhost:5433/Agents_DB"
    
    # Application Configuration
    APP_NAME: str = "Agent Management System"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings() 


