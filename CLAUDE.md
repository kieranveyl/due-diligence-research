# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Package Management
```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --dev

# Add new package
uv add package-name

# Run Python commands
uv run python script.py
```

### Testing
```bash
# Run all tests
uv run pytest

# Run unit tests only
uv run pytest tests/unit/ -v

# Run integration tests
uv run pytest tests/integration/ -v

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

### Code Quality
```bash
# Format code
uv run black src/ tests/

# Sort imports
uv run isort src/ tests/

# Lint with ruff
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

### Running the Application

#### CLI Interface
```bash
# Show configuration
uv run python -m src.cli.main config show

# Run research task
uv run python -m src.cli.main research run "Tesla Inc"

# List reports
uv run python -m src.cli.main reports list
```

#### API Server
```bash
# Start development server
uv run uvicorn src.api.main:app --host 0.0.0.0 --port 8001 --reload

# Health check
curl http://localhost:8001/health
```

#### Individual Agent Testing
```bash
# Test agents individually
uv run python -c "
from src.agents.task_agents.research import ResearchAgent
agent = ResearchAgent()
print('Research agent initialized')
"
```

## Architecture Overview

### Core Structure
- **Multi-Agent System**: 5 specialized AI agents (Research, Financial, Legal, OSINT, Verification)
- **LangGraph Orchestration**: Stateful workflow management with checkpointing
- **Exa-First Search**: Primary search engine optimized for AI agents
- **Modern Python Stack**: Python 3.13, UV package manager, FastAPI, Rich CLI

### Key Directories
```
src/
├── agents/           # AI agent implementations
│   ├── task_agents/  # Specialized agents (research, financial, legal, osint, verification)
│   └── base.py       # Base agent classes
├── api/              # FastAPI backend
├── cli/              # Click-based CLI interface
├── config/           # Configuration management
├── workflows/        # LangGraph workflow definitions
├── state/            # State management and data models
├── tools/            # External API integrations (Exa, Tavily, OpenAI)
├── security/         # Security features (encryption, monitoring, audit)
└── memory/           # Memory and persistence layers
```

### Agent Architecture
Each agent follows a consistent pattern:
- **5 Exa AI Tools**: Neural search, auto search, keyword search, comprehensive search, similarity search
- **1 Tavily Tool**: Breaking news only (minimal usage)
- **Specialized Focus**: Domain-specific search strategies and result processing
- **State Management**: LangGraph integration for workflow coordination

### Search Strategy (Exa-First)
The system prioritizes Exa AI for 95%+ of searches:
- **Neural Search**: Semantic understanding with full content extraction
- **Auto Search**: Intelligent search strategy selection
- **Keyword Search**: Precise term matching
- **Large Result Sets**: Up to 50 results per search with highlights
- **Domain Filtering**: Targeting authoritative sources

Tavily is relegated to urgent breaking news only (3 results maximum).

### Workflow Management
- **LangGraph**: Handles agent orchestration and state management
- **PostgreSQL Checkpointing**: Persistent workflow state
- **Session Management**: Encrypted session data with audit trails
- **Real-time Streaming**: WebSocket support for live updates

## Configuration

### Required Environment Variables
```bash
# Core API Keys
OPENAI_API_KEY=sk-your-openai-key
EXA_API_KEY=your-exa-key

# Optional APIs  
TAVILY_API_KEY=your-tavily-key
LANGSMITH_API_KEY=your-langsmith-key

# Database
POSTGRES_URL=postgresql://user:pass@localhost:5432/dbname
# Or SQLite: sqlite:///data/due_diligence.db

# Security
SESSION_ENCRYPTION_KEY=your-32-byte-hex-key
```

### Configuration Files
- `.env`: Environment variables
- `pyproject.toml`: Package configuration and dependencies
- `src/config/settings.py`: Application settings with validation

## Development Patterns

### Agent Development
When creating or modifying agents:
1. Inherit from base agent classes in `src/agents/base.py`
2. Implement 5 Exa tools + 1 minimal Tavily tool
3. Use consistent naming: `exa_{domain}_{search_type}`
4. Focus on domain-specific search strategies
5. Integrate with LangGraph state management

### Tool Integration
New tools should:
- Follow the LangChain tool interface
- Include comprehensive docstrings
- Handle errors gracefully with fallbacks
- Use type hints for parameters
- Include usage examples in docstrings

### Workflow Extension
When extending workflows:
- Use LangGraph's stateful graph architecture
- Implement proper checkpointing for resumability
- Handle human-in-the-loop interactions
- Include proper error handling and recovery
- Maintain audit trails for compliance

### Testing Strategy
- **Unit Tests**: Individual agent and tool functionality
- **Integration Tests**: End-to-end workflow execution
- **Mock Data**: Use when API keys unavailable
- **Performance Tests**: Benchmark search and processing times

## Security Considerations

### Data Handling
- All session data is encrypted at rest
- API keys are managed through environment variables only
- Audit logging for all agent actions
- No sensitive data in logs or error messages

### API Security
- Rate limiting on external API calls
- Secure credential management
- Input validation and sanitization
- CORS configuration for web API

### Monitoring
- Security event logging
- Performance monitoring with LangSmith
- Error tracking and alerting
- Resource usage monitoring

## Performance Optimization

### Search Efficiency
- Exa AI provides sub-450ms response times
- Batch processing for multiple queries
- Result caching with Redis (optional)
- Intelligent retry mechanisms

### Memory Management
- Streaming results for large datasets
- Checkpoint compression for long workflows
- Garbage collection for completed sessions
- Resource pooling for database connections

## Common Development Tasks

### Adding a New Agent
1. Create new file in `src/agents/task_agents/`
2. Inherit from appropriate base class
3. Implement required Exa tools
4. Add agent to workflow configuration
5. Write comprehensive tests

### Modifying Search Behavior
1. Update tool configurations in agent files
2. Adjust result limits and filtering
3. Test with various query types
4. Update documentation

### Extending API Endpoints
1. Add new routes in `src/api/main.py`
2. Define request/response models
3. Implement proper error handling
4. Add OpenAPI documentation

### CLI Command Development
1. Add command in `src/cli/commands/`
2. Register in `src/cli/main.py`
3. Follow Click patterns for consistency
4. Include help text and examples