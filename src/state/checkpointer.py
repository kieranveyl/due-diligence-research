import os

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from src.config.settings import settings


class CheckpointerFactory:
    _instance = None
    _context_manager = None

    @classmethod
    async def get_checkpointer(cls):
        """Get singleton checkpointer instance with proper lifecycle management"""
        if cls._instance is None:
            cls._instance, cls._context_manager = await cls._create_checkpointer()
        return cls._instance

    @staticmethod
    async def _create_checkpointer():
        """Create appropriate checkpointer based on environment"""
        if settings.environment == "production" and settings.postgres_url:
            checkpointer_cm = AsyncPostgresSaver.from_conn_string(
                settings.postgres_url,
                schema="langgraph_checkpoints"
            )
        else:
            # Default to SQLite for development
            os.makedirs("./data", exist_ok=True)
            checkpointer_cm = AsyncSqliteSaver.from_conn_string("./data/checkpoints.db")

        # Enter the context manager and keep reference
        checkpointer = await checkpointer_cm.__aenter__()
        await checkpointer.setup()

        # Return both the checkpointer and context manager for lifecycle management
        return checkpointer, checkpointer_cm

    @staticmethod
    async def create_checkpointer():
        """Create appropriate checkpointer based on environment"""
        checkpointer = await CheckpointerFactory.get_checkpointer()
        return checkpointer

# Export factory instance
checkpointer_factory = CheckpointerFactory()
