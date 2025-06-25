"""Main FastAPI Application"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings
from app.database.connection import init_db, close_db
from app.api.routes import router
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Start app
    try:
        await init_db()
        logger.info("Database initialized succuessfully!")
    except Exception as e:
        logger.warning(f"Database initialization failed: {e}")
        logger.info("Application will start without database initialization")
        
    yield
    # Shutdown app
    try:
        await close_db()
        logger.info("Database connection closed.")
    except Exception as e:
        logger.warning("Error closing database connection: {e}")
        

# Create FastAPI Application
app = FastAPI(
    title=settings.app_name,
    description="A comprehensive API for managing intelligence agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(router)


@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {
        "message": "Welcome to Agent Management System",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "agent-management-system"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    ) 