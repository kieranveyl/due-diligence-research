# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-agent due diligence system built with LangGraph for comprehensive research on people, companies, and entities. The system uses specialized agents coordinated through a graph-based workflow to perform parallel research tasks and synthesize findings into comprehensive reports.

## Common Development Commands

### Environment Setup
```bash
# Copy environment file and configure API keys
cp .env.example .env
# Edit .env with your API keys (OpenAI, Anthropic, Tavily, Exa)

# Install dependencies with uv
uv sync

# Run automated setup (starts Docker services)
python scripts/setup.py
```

### Running the Application
```bash
# Development mode with hot reload
uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Or with Docker
docker-compose up
```

### Testing
```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=html

# Run specific test categories
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -v
```

### Code Quality
```bash
# Format code
uv run black src/ tests/

# Sort imports
uv run isort src/ tests/

# Type checking
uv run mypy src/

# Linting
uv run ruff check src/ tests/
```

### Database Management
```bash
# Start database services
docker-compose up -d postgres redis

# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d duediligence
```

## Architecture Overview

### Multi-Agent System
The system follows a graph-based architecture with specialized agents:

- **Supervisor Agent** (`src/agents/supervisor.py`): Top-level orchestrator that routes queries and coordinates handoffs
- **Planning Agent** (`src/agents/planner.py`): Decomposes complex queries into parallel research tasks
- **Task Agents** (`src/agents/task_agents/`): Specialized workers for different research domains
  - Research Agent: Web research and information gathering
  - Financial Agent: Financial data and analysis (planned)
  - Legal Agent: Legal documents and compliance (planned)
  - OSINT Agent: Digital footprint analysis (planned)
  - Verification Agent: Fact-checking and source validation (planned)

### State Management
- **Global State** (`src/state/definitions.py`): Centralized state using `DueDiligenceState` TypedDict
- **Checkpointing** (`src/state/checkpointer.py`): Persistent state with PostgreSQL/SQLite support
- **Task Tracking**: Individual research tasks with status, results, and citations

### Workflow Orchestration
- **LangGraph StateGraph** (`src/workflows/due_diligence.py`): Defines agent relationships and execution flow
- **Parallel Execution**: Tasks run concurrently for optimal performance
- **Context Isolation**: Each agent receives focused context to prevent token overflow

### API Layer
- **FastAPI Application** (`src/api/main.py`): RESTful API with streaming support
- **Server-Sent Events**: Real-time progress streaming via `/research/{thread_id}/stream`
- **Thread Management**: Persistent research sessions with resumable execution

## Key Development Patterns

### Adding New Agents
1. Create agent class in `src/agents/task_agents/`
2. Implement `create_agent()` method returning LangGraph agent
3. Add handoff tool in `SupervisorAgent._create_handoff_tools()`
4. Register in workflow graph (`src/workflows/due_diligence.py`)

### Task Execution Pattern
- Tasks use two-tier retrieval: snippet analysis → full content extraction
- Results follow structured output schemas defined in planning phase
- Each task includes confidence scoring and citation tracking

### State Updates
- All state changes go through the central `DueDiligenceState`
- Use immutable updates: `{**state, "new_field": value}`
- Leverage LangGraph's built-in checkpointing for persistence

### Error Handling
- Agents include fallback mechanisms for API failures
- Circuit breakers and retry logic in data source integrations
- Graceful degradation when tools are unavailable

## Configuration

### Environment Variables (Required)
```bash
# API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
TAVILY_API_KEY=your_tavily_key
EXA_API_KEY=your_exa_key

# Database URLs
POSTGRES_URL=postgresql+asyncpg://user:pass@localhost/duediligence
REDIS_URL=redis://localhost:6379/0

# Application Settings
ENVIRONMENT=development|production
DEFAULT_MODEL=gpt-4o-mini
DEFAULT_TEMPERATURE=0.1
```

### Model Configuration
- Default model: `gpt-4o-mini` (configurable via `DEFAULT_MODEL`)
- Temperature: `0.1` for consistent, factual outputs
- Context window management: 8000 tokens with compression at 6000

## Data Sources Integration

The system integrates multiple external APIs:
- **Tavily**: Advanced web search and content extraction
- **Exa**: AI-powered search for high-quality sources
- **OpenAI/Anthropic**: LLM inference for analysis and synthesis
- **LangSmith**: Optional tracing and performance monitoring

## Testing Strategy

### Unit Tests (`tests/unit/`)
- Individual agent functionality
- State transformations
- Utility functions

### Integration Tests (`tests/integration/`)
- End-to-end workflow execution
- API endpoint testing
- Database interaction tests

### Test Configuration
- Uses pytest with asyncio support
- Coverage reporting with pytest-cov
- Fixtures defined in `conftest.py`

## Production Considerations

### Deployment
- Docker Compose for local development
- Kubernetes manifests available in project
- Health checks at `/health` endpoint

### Monitoring
- Structured logging with correlation IDs
- Prometheus metrics (if configured)
- LangSmith integration for LLM observability

### Security
- API keys via environment variables only
- Input validation on all endpoints
- Rate limiting considerations for external APIs

## Troubleshooting

### Common Issues
1. **Missing API Keys**: Ensure all required API keys are set in `.env`
2. **Database Connection**: Verify PostgreSQL/Redis services are running
3. **Tool Initialization**: Check API key validity for external services
4. **Memory Issues**: Monitor context window usage in complex queries

### Development Tips
- Use dummy tools when API keys unavailable (see `ResearchAgent._initialize_tools()`)
- Enable debug logging: `LOG_LEVEL=DEBUG`
- Test individual agents before full workflow integration
- Use thread-specific configs for concurrent development testing