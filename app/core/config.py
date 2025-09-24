from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    postgres_url: str = "postgresql://postgres:password123@localhost:5432/fastapi_langgraph_db"
    
    # API Keys
    google_api_key: str = ""
    
    # App
    app_name: str = "FastAPI LangGraph Backend"
    app_version: str = "0.1.0"
    debug: bool = True
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Rate Limiting
    rate_limit_requests: int = 10
    
    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://localhost:8080"]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
