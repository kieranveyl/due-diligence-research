# Due Diligence System v2.0 - Operational Runbook

## Table of Contents
1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Installation & Setup](#installation--setup)
4. [Configuration](#configuration)
5. [Running the System](#running-the-system)
6. [Agent Architecture](#agent-architecture)
7. [API Integration Guide](#api-integration-guide)
8. [Troubleshooting](#troubleshooting)
9. [Monitoring & Logging](#monitoring--logging)
10. [Security Operations](#security-operations)
11. [Maintenance](#maintenance)

---

## System Overview

The Due Diligence System v2.0 is a multi-agent AI platform for comprehensive business intelligence and risk assessment. Built on Python 3.13 with LangGraph orchestration, it leverages **Exa AI as the primary search engine** with minimal Tavily backup for breaking news.

### Architecture Highlights
- **5 Specialized Agents**: Research, Financial, Legal, OSINT, Verification
- **Exa-First Design**: 95%+ searches use Exa's neural, auto, and keyword capabilities
- **LangChain Integration**: Full content extraction with highlights
- **Modern Stack**: Python 3.13, UV package manager, Rich CLI, FastAPI
- **Security**: Session encryption, audit logging, monitoring

---

## Prerequisites

### System Requirements
- **Python**: 3.10+ (3.13 recommended)
- **UV Package Manager**: Latest version
- **Database**: PostgreSQL or SQLite
- **Redis**: For caching (optional)
- **Memory**: 4GB+ RAM
- **Storage**: 2GB+ free space

### API Keys Required
- **OpenAI API Key**: For LLM orchestration
- **Exa API Key**: Primary search engine
- **Tavily API Key**: Auxiliary breaking news (optional)
- **LangSmith API Key**: Observability (optional)

---

## Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd due-diligence-exa/.conductor/migration-v2
```

### 2. Install UV Package Manager
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Install Dependencies
```bash
# Install all dependencies using UV
uv sync

# Verify installation
uv run python --version  # Should show Python 3.13.x
```

### 4. Verify Installation
```bash
# Test core imports
uv run python -c "
from src.agents.task_agents.research import ResearchAgent
from src.workflows.due_diligence import DueDiligenceWorkflow
print('✅ Installation successful!')
"
```

---

## Configuration

### 1. Environment Variables
Create `.env` file in project root:

```bash
# Core API Keys
OPENAI_API_KEY=sk-your-openai-key-here
EXA_API_KEY=your-exa-api-key-here
TAVILY_API_KEY=your-tavily-key-here  # Optional

# Database
POSTGRES_URL=postgresql://user:pass@localhost:5432/dbname
# OR for SQLite
POSTGRES_URL=sqlite:///data/due_diligence.db

# Optional Services
REDIS_URL=redis://localhost:6379/0
LANGSMITH_API_KEY=your-langsmith-key  # For observability

# Security
SESSION_ENCRYPTION_KEY=your-32-byte-hex-key
AUDIT_LOG_LEVEL=INFO
```

### 2. Generate Encryption Key
```bash
uv run python -c "
import secrets
print('SESSION_ENCRYPTION_KEY=' + secrets.token_hex(32))
"
```

### 3. Configuration Validation
```bash
# Validate all API keys and settings
uv run python -c "
from src.config.settings import settings
print('✅ OpenAI:', '✅' if settings.has_openai_key else '❌')
print('✅ Exa:', '✅' if settings.has_exa_key else '❌') 
print('✅ Tavily:', '✅' if settings.has_tavily_key else '❌')
print('✅ Database:', '✅' if settings.postgres_url else '❌')
"
```

---

## Running the System

### 1. CLI Interface
```bash
# Show configuration
uv run python -m src.cli.main config show

# Run research task
uv run python -m src.cli.main research run "Tesla Inc acquisition analysis"

# List available reports
uv run python -m src.cli.main reports list

# Generate financial analysis
uv run python -m src.cli.main financial analyze "Tesla Inc" --output-format json
```

### 2. Individual Agent Testing
```bash
# Test Research Agent (Exa-powered)
uv run python test_research_agent.py

# Test Financial Agent
uv run python test_financial_agent.py

# Test Legal Agent
uv run python test_legal_agent.py

# Test OSINT Agent
uv run python test_osint_agent.py

# Test Verification Agent
uv run python test_verification_agent.py
```

### 3. Full Workflow Execution
```bash
# Run complete due diligence workflow
uv run python -c "
import asyncio
from src.workflows.due_diligence import DueDiligenceWorkflow

async def main():
    workflow = DueDiligenceWorkflow()
    async for event in workflow.run(
        query='Comprehensive due diligence on Tesla Inc',
        entity_type='company',
        entity_name='Tesla Inc'
    ):
        print(f'Event: {event}')

asyncio.run(main())
"
```

### 4. Run Tests
```bash
# Unit tests
uv run pytest tests/unit/ -v

# Integration tests  
uv run pytest tests/integration/ -v

# All tests
uv run pytest -v
```

---

## Agent Architecture

### Exa-First Search Strategy

All agents now prioritize **Exa AI** for 95%+ of searches, with Tavily relegated to auxiliary breaking news only.

#### Research Agent
```python
# 5 Exa Tools + 1 Minimal Tavily
- exa_neural_search (15 results, full content + highlights)
- exa_auto_search (12 results, intelligent strategy)
- exa_keyword_search (10 results, precise terms)
- exa_comprehensive_search (50 results, due diligence)
- exa_find_similar (8 results, expansion)
- tavily_breaking_news (3 results, urgent only)
```

#### Financial Agent
```python
# 5 Exa Tools + 1 Minimal Tavily
- exa_sec_filings_neural (20 results, SEC focus)
- exa_financial_comprehensive (40 results, broad analysis)
- exa_earnings_reports (15 results, earnings focus)
- exa_financial_keyword (12 results, metrics/ratios)
- exa_find_similar_financial (10 results, comparisons)
- tavily_urgent_market_updates (3 results, immediate only)
```

#### Legal Agent
```python
# 5 Exa Tools + 1 Minimal Tavily
- exa_legal_comprehensive (35 results, full legal landscape)
- exa_court_records (20 results, case law focus)
- exa_regulatory_compliance (18 results, enforcement)
- exa_legal_keyword (12 results, citations/statutes)
- exa_find_similar_legal (10 results, precedents)
- tavily_urgent_legal_news (3 results, breaking only)
```

#### OSINT Agent
```python
# 5 Exa Tools + 1 Minimal Tavily
- exa_osint_comprehensive (40 results, digital footprint)
- exa_public_records (25 results, official records)
- exa_reputation_monitoring (30 results, sentiment analysis)
- exa_osint_keyword (15 results, specific identifiers)
- exa_find_similar_digital_assets (12 results, related entities)
- tavily_urgent_osint (3 results, breaking developments)
```

#### Verification Agent
```python
# 5 Exa Tools + 1 Minimal Tavily
- exa_authoritative_comprehensive (30 results, official sources)
- exa_primary_sources_neural (25 results, original documents)
- exa_verification_keyword (15 results, specific claims)
- exa_academic_sources (20 results, scholarly verification)
- exa_find_corroborating_sources (12 results, cross-reference)
- tavily_urgent_fact_check (3 results, immediate verification)
```

### Agent Initialization
```python
from src.agents.task_agents.research import ResearchAgent

# Initialize with Exa-first configuration
agent = ResearchAgent()
print(f"Tools available: {len(agent.tools)}")
for tool in agent.tools:
    print(f"- {tool.name}")
```

---

## API Integration Guide

### Exa AI Integration (Primary)

#### Features Utilized
- **Neural Search**: Semantic understanding of queries
- **Auto Search**: Intelligent search strategy selection
- **Keyword Search**: Precise term matching
- **Large-scale Results**: Up to 50 results per search
- **Full Content**: Complete webpage extraction
- **Highlights**: Key excerpt identification
- **Domain Filtering**: Authoritative source targeting

#### Configuration Example
```python
from langchain_exa import ExaSearchResults

# Neural search with full content
exa_tool = ExaSearchResults(
    name="exa_neural_search",
    description="Deep neural search with full content",
    num_results=15,
    api_key=settings.exa_api_key,
    type="neural",
    text_contents_options=True,
    highlights=True,
    include_domains=["sec.gov", "bloomberg.com", "reuters.com"]
)
```

### Tavily Integration (Auxiliary)

Tavily is **minimized** to breaking news only:

```python
from langchain_community.tools.tavily_search import TavilySearchResults

# Minimal Tavily for urgent updates only
tavily_tool = TavilySearchResults(
    name="tavily_urgent_news",
    description="ONLY for urgent breaking news within hours",
    max_results=3,  # Minimal results
    api_wrapper_kwargs={"api_key": settings.tavily_api_key}
)
```

### OpenAI Integration
```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model=settings.default_model,  # gpt-4o-mini
    temperature=settings.default_temperature,  # 0.1
    api_key=settings.openai_api_key
)
```

---

## Troubleshooting

### Common Issues

#### 1. API Key Issues
```bash
# Error: "No module named 'langchain_exa'"
uv sync  # Reinstall dependencies

# Error: "Invalid API key"
# Check .env file and key validity
uv run python -c "from src.config.settings import settings; print(settings.exa_api_key[:10] + '...')"
```

#### 2. Agent Initialization Failures
```bash
# Error: "Using dummy tools - configure API keys"
# This is expected when API keys are missing
# Agents will work with mock data for testing

# To verify real API functionality:
export EXA_API_KEY=your-real-key
uv run python test_research_agent.py
```

#### 3. Database Connection Issues
```bash
# SQLite (default)
mkdir -p data
export POSTGRES_URL=sqlite:///data/due_diligence.db

# PostgreSQL 
export POSTGRES_URL=postgresql://user:pass@localhost:5432/dbname
```

#### 4. Workflow Compilation Errors
```python
# Ensure async compilation
workflow = DueDiligenceWorkflow()
compiled = await workflow._ensure_compiled()
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
uv run python -m src.cli.main research run "test query"
```

### Performance Issues
```bash
# Check tool performance
uv run python -c "
import time
from src.agents.task_agents.research import ResearchAgent

agent = ResearchAgent()
start = time.time()
# agent operations
print(f'Time: {time.time() - start:.2f}s')
"
```

---

## Monitoring & Logging

### Security Monitoring
```python
from src.security.monitoring import SecurityMonitor

monitor = SecurityMonitor()
await monitor.log_security_event(
    event_type="agent_execution",
    details={"agent": "research", "query": "sensitive_query"},
    risk_level="medium"
)
```

### Audit Logging
```python
from src.security.audit import AuditLogger

audit = AuditLogger()
await audit.log_action(
    action="search_execution",
    user_id="user123",
    resource="exa_api",
    details={"query": "Tesla Inc", "results": 15}
)
```

### Performance Metrics
```bash
# View agent performance
uv run python -c "
from src.agents.task_agents.research import ResearchAgent
import asyncio

async def benchmark():
    agent = ResearchAgent()
    # Benchmark operations
    pass

asyncio.run(benchmark())
"
```

---

## Security Operations

### Session Encryption
```python
from src.security.encryption import SessionEncryption

encryption = SessionEncryption()
encrypted_data = await encryption.encrypt_session_data(sensitive_data)
decrypted_data = await encryption.decrypt_session_data(encrypted_data)
```

### API Key Management
```bash
# Rotate API keys
# 1. Generate new keys from providers
# 2. Update .env file
# 3. Restart services
# 4. Verify functionality

uv run python -c "from src.config.settings import settings; print('Keys loaded:', settings.has_exa_key)"
```

### Security Audit
```python
# Run security checks
from src.security.audit import AuditLogger

audit = AuditLogger()
recent_events = await audit.get_recent_events(hours=24)
print(f"Security events in last 24h: {len(recent_events)}")
```

---

## Maintenance

### Daily Operations
```bash
# 1. Check system health
uv run pytest tests/unit/test_agents.py -v

# 2. Verify API connectivity
uv run python -c "from src.config.settings import settings; print('✅ All keys valid' if all([settings.has_openai_key, settings.has_exa_key]) else '❌ Missing keys')"

# 3. Review logs
tail -f logs/due_diligence.log
```

### Weekly Maintenance
```bash
# 1. Update dependencies
uv sync --upgrade

# 2. Run full test suite
uv run pytest -v

# 3. Database maintenance (if using PostgreSQL)
# Run VACUUM, ANALYZE, etc.

# 4. Security audit
uv run python -c "
from src.security.audit import AuditLogger
import asyncio

async def audit():
    logger = AuditLogger() 
    events = await logger.get_recent_events(hours=168)  # 1 week
    print(f'Total events: {len(events)}')

asyncio.run(audit())
"
```

### Backup & Recovery
```bash
# 1. Backup database
pg_dump due_diligence > backup_$(date +%Y%m%d).sql

# 2. Backup configuration
tar -czf config_backup_$(date +%Y%m%d).tar.gz .env src/config/

# 3. Test restore procedure
# Restore to test environment and verify functionality
```

### Scaling Operations
```bash
# Monitor performance
uv run python -c "
import psutil
print(f'CPU: {psutil.cpu_percent()}%')
print(f'Memory: {psutil.virtual_memory().percent}%')
print(f'Disk: {psutil.disk_usage(\"/\").percent}%')
"

# If scaling needed:
# 1. Increase result limits in agent configurations
# 2. Add more concurrent agents
# 3. Implement Redis caching
# 4. Consider distributed deployment
```

---

## Production Deployment Checklist

### Pre-Deployment
- [ ] All API keys configured and validated
- [ ] Database setup and migrations completed
- [ ] Security encryption keys generated
- [ ] Environment variables configured
- [ ] Tests passing (unit + integration)
- [ ] Performance benchmarks acceptable
- [ ] Monitoring and logging configured
- [ ] Backup procedures in place

### Post-Deployment
- [ ] Smoke tests completed
- [ ] API connectivity verified
- [ ] Agent functionality confirmed
- [ ] Security monitoring active
- [ ] Performance monitoring active
- [ ] Documentation updated
- [ ] Team training completed

---

## Support & Contact

### Internal Issues
- Check logs: `logs/due_diligence.log`
- Run diagnostics: `uv run pytest tests/unit/ -v`
- Review configuration: `uv run python -m src.cli.main config show`

### External Dependencies
- **Exa AI**: [docs.exa.ai](https://docs.exa.ai)
- **OpenAI**: [platform.openai.com](https://platform.openai.com)
- **Tavily**: [tavily.com](https://tavily.com)
- **LangChain**: [python.langchain.com](https://python.langchain.com)

---

*This runbook covers the complete operational lifecycle of the Due Diligence System v2.0 with its Exa-first architecture. For technical implementation details, see the codebase documentation.*