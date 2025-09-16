# Due Diligence System Runbook

This runbook documents how the actual due diligence multi-agent system works after debugging and fixing all blocking issues.

## System Overview

The system is a multi-agent due diligence research platform built with LangGraph that:

- Accepts research queries through a REST API
- Decomposes queries into parallel tasks using a planning agent
- Executes tasks using specialized agents (research, financial, legal, etc.)
- Streams real-time results via Server-Sent Events
- Persists workflow state using async SQLite checkpointing

## Starting the System

### Prerequisites

```bash
# Ensure dependencies are installed
uv sync

# Verify environment file exists with API keys
cat .env
```

### Start the Server

```bash
# Development mode with hot reload
uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uv run uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

### Verify Health

```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","version":"1.0.0"}
```

## API Endpoints

### 1. Health Check

```bash
GET /health
# Returns server health status
```

### 2. Start Research

```bash
POST /research
Content-Type: application/json

{
  "query": "Research ABC Corporation for potential acquisition",
  "entity_type": "company",
  "entity_name": "ABC Corporation",
  "thread_id": "optional-custom-id"
}

# Returns:
{
  "thread_id": "uuid-string",
  "status": "started",
  "stream_url": "/research/{thread_id}/stream"
}
```

### 3. Stream Results

```bash
GET /research/{thread_id}/stream
# Returns Server-Sent Events stream with real-time progress
```

### 4. Check Status

```bash
GET /research/{thread_id}/status
# Returns current workflow status
```

## Workflow Execution Flow

### 1. Request Processing

- API receives research request
- Creates unique thread ID for session
- Initializes workflow state
- Returns stream URL immediately

### 2. Supervisor Agent

- First agent to receive the query
- Analyzes request and determines routing
- Coordinates handoffs between agents

### 3. Planning Agent

- Decomposes query into parallel research tasks
- Analyzes complexity and estimates time
- Creates task specifications with assigned agents
- Returns structured research plan

### 4. Task Executor

- Manages parallel execution of research tasks
- Batches tasks to control concurrency (max 3 parallel)
- Routes tasks to appropriate specialized agents
- Aggregates results from completed tasks

### 5. Specialized Agents

- **Research Agent**: Web research and information gathering
- **Financial Agent**: Financial data, SEC filings, market analysis
- **Legal Agent**: Legal compliance, regulatory issues
- **OSINT Agent**: Digital footprint analysis
- **Verification Agent**: Fact-checking and source validation

### 6. State Management

- All workflow state persists in SQLite database
- Supports resumable execution via checkpointing
- Thread-specific isolation
- Automatic state recovery on restart

## Real-Time Streaming

### Event Format

```javascript
// Server-Sent Events format
data: {"supervisor": {"messages": [...]}}
data: {"planner": {"research_plan": "...", "tasks": [...]}}
data: {"task_executor": {"completed_tasks": 3, "total_tasks": 5}}
data: {"error": "Error message if something fails"}
```

### Event Types

- **Agent responses**: Messages from individual agents
- **State updates**: Changes to workflow state
- **Task progress**: Task completion status
- **Errors**: Any execution failures with details

## Configuration

### Environment Variables

```bash
# Required for production
OPENAI_API_KEY=your_openai_key
EXA_API_KEY=your_exa_key
ANTHROPIC_API_KEY=your_anthropic_key

# Optional for development
POSTGRES_URL=postgresql+asyncpg://user:pass@localhost/duediligence
REDIS_URL=redis://localhost:6379/0

# Application settings
ENVIRONMENT=development
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
```

### Data Storage

- **SQLite**: Default for development (`./data/checkpoints.db`)
- **PostgreSQL**: Production checkpointing (if configured)
- **File System**: Chroma vector database (`./data/chroma/`)

## Debugging and Monitoring

### Debug Endpoints

```bash
# Test workflow initialization
GET /debug/workflow

# Test simple workflow execution
GET /debug/simple-run
```

### Common Issues and Solutions

#### 1. Database Connection Errors

**Error**: `Cannot operate on a closed database`
**Solution**: Restart server to reinitialize async SQLite connection

#### 2. JSON Serialization Errors

**Error**: `Object of type AIMessage is not JSON serializable`
**Solution**: Fixed with `_make_serializable()` function handling complex objects

#### 3. Missing Dependencies

**Error**: `AsyncSqliteSaver requires aiosqlite package`
**Solution**: `uv add aiosqlite`

#### 4. API Key Issues

**Error**: OpenAI/Exa API failures
**Solution**: Verify API keys in `.env` file, agents fallback to dummy tools

### Monitoring Logs

```bash
# View server logs in real-time
tail -f logs/application.log

# Check for specific errors
grep "ERROR" logs/application.log
```

## Production Deployment

### Docker Deployment

```bash
# Start services
docker-compose up -d

# Check status
docker-compose ps
```

### Environment Setup

1. Set `ENVIRONMENT=production`
2. Configure PostgreSQL URL
3. Set all required API keys
4. Enable monitoring/logging

### Health Checks

- Health endpoint: `/health`
- Database connectivity check
- API key validation
- Memory usage monitoring

## Testing the System

### Basic Functionality Test

```bash
# 1. Start research
THREAD_ID=$(curl -s -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"query": "Test query", "entity_type": "company", "entity_name": "Test Corp"}' \
  | jq -r '.thread_id')

# 2. Stream results
curl http://localhost:8000/research/$THREAD_ID/stream

# 3. Check status
curl http://localhost:8000/research/$THREAD_ID/status
```

### Expected Behavior

1. Research request returns immediately with thread ID
2. Streaming shows supervisor agent response
3. Planning agent creates research plan
4. Task executor processes parallel tasks
5. Specialized agents execute assigned tasks
6. Final results aggregated and returned

## Architecture Notes

### Key Components

- **FastAPI**: HTTP server with async support
- **LangGraph**: Multi-agent workflow orchestration
- **AsyncSqliteSaver**: Persistent state management
- **OpenAI GPT-4**: LLM for agent reasoning
- **Exa Search**: Advanced web research capabilities

### Design Patterns

- **State Machine**: LangGraph manages workflow transitions
- **Event Streaming**: Real-time progress via Server-Sent Events
- **Checkpointing**: Automatic state persistence and recovery
- **Agent Delegation**: Supervisor routes tasks to specialists
- **Parallel Execution**: Concurrent task processing for efficiency

### Performance Considerations

- Max 3 parallel tasks to control resource usage
- Async operations throughout the stack
- Connection pooling for database access
- Stream buffering for large responses

## Troubleshooting

### System Not Starting

1. Check Python/uv installation
2. Verify dependencies: `uv sync`
3. Check port availability: `lsof -i :8000`
4. Review environment variables

### Workflow Failures

1. Check API key validity
2. Verify network connectivity
3. Review agent configuration
4. Check database permissions

### Performance Issues

1. Monitor concurrent task limits
2. Check database connection pool
3. Review memory usage
4. Optimize agent prompts

## Success Metrics

The system is working correctly when:

- ✅ Health endpoint returns 200 status
- ✅ Research requests return thread IDs immediately
- ✅ Streaming shows progressive agent responses
- ✅ Workflow completes without connection errors
- ✅ Results include structured research findings
- ✅ State persists across server restarts

## Support

For issues or questions:

1. Check logs for error details
2. Use debug endpoints for diagnostics
3. Verify configuration matches this runbook
4. Test with minimal examples first
