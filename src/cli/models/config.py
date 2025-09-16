"""Configuration models for CLI"""

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class CLIConfig(BaseModel):
    """CLI configuration settings"""

    # Output settings
    default_output_dir: str = Field(default="./reports", description="Default reports directory")
    default_format: str = Field(default="markdown", description="Default output format")

    # Research settings
    default_scope: list[str] = Field(default=["financial", "legal", "osint", "verification"], description="Default research scope")
    confidence_threshold: float = Field(default=0.8, ge=0.0, le=1.0, description="Minimum confidence threshold")
    max_sources: int = Field(default=50, ge=1, le=200, description="Maximum sources per research")
    timeout: int = Field(default=300, ge=60, le=3600, description="Research timeout in seconds")

    # Model settings
    model: str = Field(default="gpt-4o-mini", description="Default LLM model")
    parallel_tasks: int = Field(default=3, ge=1, le=10, description="Max parallel tasks")

    # API settings
    auto_validate_keys: bool = Field(default=True, description="Auto-validate API keys")

    @classmethod
    def get_config_path(cls) -> Path:
        """Get configuration file path"""
        config_dir = Path.home() / ".config" / "due-diligence"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "config.json"

    @classmethod
    def load(cls) -> "CLIConfig":
        """Load configuration from file"""
        config_path = cls.get_config_path()
        if config_path.exists():
            try:
                with open(config_path) as f:
                    data = json.load(f)
                return cls(**data)
            except Exception:
                # Return default config if file is corrupted
                return cls()
        return cls()

    def save(self) -> None:
        """Save configuration to file"""
        config_path = self.get_config_path()
        with open(config_path, 'w') as f:
            json.dump(self.model_dump(), f, indent=2)

    def update(self, **kwargs) -> None:
        """Update configuration values"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def reset(self) -> None:
        """Reset to default configuration"""
        default_config = CLIConfig()
        for field in self.model_fields:
            setattr(self, field, getattr(default_config, field))
        self.save()


class SessionData(BaseModel):
    """Research session data for persistence"""

    session_id: str
    entity_name: str
    entity_type: str
    query: str
    scope: list[str]
    status: str = "pending"  # pending, running, completed, failed
    created_at: str
    completed_at: str | None = None
    report_path: str | None = None
    confidence: float | None = None
    sources_count: int | None = None

    @classmethod
    def get_sessions_path(cls) -> Path:
        """Get sessions directory path"""
        sessions_dir = Path.home() / ".config" / "due-diligence" / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        return sessions_dir

    def save(self) -> None:
        """Save session data"""
        sessions_path = self.get_sessions_path()
        session_file = sessions_path / f"{self.session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(self.model_dump(), f, indent=2)

    @classmethod
    def load(cls, session_id: str) -> Optional["SessionData"]:
        """Load session data by ID"""
        sessions_path = cls.get_sessions_path()
        session_file = sessions_path / f"{session_id}.json"
        if session_file.exists():
            try:
                with open(session_file) as f:
                    data = json.load(f)
                return cls(**data)
            except Exception:
                return None
        return None

    @classmethod
    def list_sessions(cls) -> list["SessionData"]:
        """List all saved sessions"""
        sessions_path = cls.get_sessions_path()
        sessions = []
        for session_file in sessions_path.glob("*.json"):
            try:
                with open(session_file) as f:
                    data = json.load(f)
                sessions.append(cls(**data))
            except Exception:
                continue
        return sorted(sessions, key=lambda s: s.created_at, reverse=True)
