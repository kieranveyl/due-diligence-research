import uuid
from datetime import datetime
from enum import Enum
from typing import Annotated, Any, TypedDict

from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class EntityType(Enum):
    PERSON = "person"
    COMPANY = "company"
    PLACE = "place"
    CUSTOM = "custom"

class ResearchTask(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    priority: int = Field(ge=1, le=10, default=5)
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: str
    output_schema: dict[str, Any] = Field(default_factory=dict)
    results: dict[str, Any] = Field(default_factory=dict)
    citations: list[str] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None

class DueDiligenceState(TypedDict):
    """Global state for the due diligence system"""
    # Core conversation
    messages: Annotated[list, add_messages]

    # Query information
    query: str
    entity_type: EntityType
    entity_name: str

    # Task management
    tasks: list[ResearchTask]
    research_plan: str

    # Results
    raw_findings: dict[str, Any]
    synthesized_report: str
    citations: list[str]
    confidence_scores: dict[str, float]

    # Metadata
    thread_id: str
    session_id: str
    user_id: str | None
    metadata: dict[str, Any]

    # Control flags
    ready_for_synthesis: bool
    human_feedback_required: bool
    completed: bool
