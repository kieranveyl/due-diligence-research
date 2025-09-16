import os

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Keys - Optional for development, required for production
    openai_api_key: str | None = Field(None, env="OPENAI_API_KEY")
    anthropic_api_key: str | None = Field(None, env="ANTHROPIC_API_KEY")
    exa_api_key: str | None = Field(None, env="EXA_API_KEY")
    tavily_api_key: str | None = Field(None, env="TAVILY_API_KEY")
    langsmith_api_key: str | None = Field(None, env="LANGSMITH_API_KEY")

    # Database - Optional for local development
    postgres_url: str | None = Field(None, env="POSTGRES_URL")
    redis_url: str | None = Field(None, env="REDIS_URL")

    # Application
    environment: str = Field("development", env="ENVIRONMENT")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")

    # Vector Database
    chroma_persist_directory: str = Field("./data/chroma", env="CHROMA_PERSIST_DIRECTORY")

    # Model Configuration
    default_model: str = Field("gpt-4o-mini", env="DEFAULT_MODEL")
    default_temperature: float = Field(0.1, env="DEFAULT_TEMPERATURE")

    # System Limits
    max_tasks_per_query: int = Field(10, env="MAX_TASKS_PER_QUERY")
    max_parallel_tasks: int = Field(5, env="MAX_PARALLEL_TASKS")
    context_window_size: int = Field(8000, env="CONTEXT_WINDOW_SIZE")

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.environment.lower() in ("development", "dev", "local")

    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.environment.lower() in ("production", "prod")

    def validate_required_keys(self) -> list[str]:
        """Validate required API keys and return missing ones"""
        missing = []
        if self.is_production:
            if not self.openai_api_key:
                missing.append("OPENAI_API_KEY")
            if not self.exa_api_key:
                missing.append("EXA_API_KEY")
            if not self.postgres_url:
                missing.append("POSTGRES_URL")
            if not self.redis_url:
                missing.append("REDIS_URL")
        return missing

    @property
    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is available"""
        return bool(self.openai_api_key and self.openai_api_key != "your_openai_key_here")

    @property
    def has_exa_key(self) -> bool:
        """Check if Exa API key is available"""
        return bool(self.exa_api_key and self.exa_api_key != "your_exa_key_here")

    @property
    def has_anthropic_key(self) -> bool:
        """Check if Anthropic API key is available"""
        return bool(self.anthropic_api_key and self.anthropic_api_key != "your_anthropic_key_here")

    @property
    def has_tavily_key(self) -> bool:
        """Check if Tavily API key is available"""
        return bool(self.tavily_api_key and self.tavily_api_key != "your_tavily_key_here")

    @property
    def has_langsmith_key(self) -> bool:
        """Check if LangSmith API key is available"""
        return bool(self.langsmith_api_key and self.langsmith_api_key != "your_langsmith_key_here")

# Global settings instance
try:
    settings = Settings()
    # Log missing keys in production
    if settings.is_production:
        missing_keys = settings.validate_required_keys()
        if missing_keys:
            raise ValueError(f"Missing required environment variables in production: {', '.join(missing_keys)}")
except Exception as e:
    if os.getenv("ENVIRONMENT", "development").lower() in ("production", "prod"):
        raise e
    else:
        # In development, create settings with defaults even if validation fails
        settings = Settings()
