import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost:5433/Agents_DB")
    
    


