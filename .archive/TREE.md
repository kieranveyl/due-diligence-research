# Due Diligence EXA - Project Structure Analysis

## Project Overview

This is a comprehensive due diligence research system that combines multiple AI agents, a CLI interface, an API backend, and workflow orchestration to conduct automated research on entities (companies, individuals, etc.).

## Root Directory Structure

```
due-diligence-exa/
├── pyproject.toml              # Python project configuration, dependencies, CLI entry points
├── uv.lock                     # UV package manager lock file for reproducible builds
├── README.md                   # Project documentation and getting started guide
├── CHANGELOG.md                # Version history and feature changes
├── TREE.md                     # This file - project structure documentation
├── .env.example               # Environment variables template for API keys
├── .gitignore                 # Git ignore patterns for Python projects
├── src/                       # Main source code directory
├── tests/                     # Test suite directory
├── docs/                      # User and developer documentation
├── scripts/                   # Utility scripts for development and deployment
├── reports/                   # Default output directory for generated reports
└── sessions/                  # Stored research session data
```

## Source Code Architecture (`src/`)

### CLI Module (`src/cli/`)

**Purpose**: Modern command-line interface for interactive research operations

```
src/cli/
├── __init__.py               # CLI module initialization
├── main.py                   # Primary CLI entry point with Click framework
├── commands/                 # CLI command implementations
│   ├── __init__.py
│   ├── config.py            # Configuration management commands (show, set, validate)
│   ├── reports.py           # Report management (list, show, export, cleanup)
│   ├── research.py          # Research execution commands (run, status)
│   └── utils.py             # CLI utility functions (entity detection, validation)
├── models/                   # Data models for CLI operations
│   ├── __init__.py
│   └── config.py            # Configuration and session persistence models
└── ui/                       # Rich UI components for enhanced CLI experience
    ├── __init__.py
    └── progress.py          # Progress tracking, interactive prompts, result display
```

**Key Features**:

- Interactive research workflow with real-time progress
- Session persistence for long-running tasks
- Configuration management with API key validation
- Report generation and management
- Graceful fallback to demo mode when APIs unavailable

### Agent System (`src/agents/`)

**Purpose**: Specialized AI agents for different types of research analysis

```
src/agents/
├── __init__.py               # Agent module exports
├── base.py                   # Abstract base agent class with common functionality
├── financial.py             # Financial analysis agent for company metrics, filings
├── legal.py                  # Legal research agent for compliance, litigation
├── osint.py                  # Open source intelligence gathering agent
├── research.py              # General research coordination agent
└── verification.py          # Fact-checking and verification agent
```

**Key Features**:

- Each agent specializes in specific research domains
- Common base class ensures consistent interface
- Integration with LangGraph for workflow orchestration
- Configurable confidence thresholds and source limits

### API Backend (`src/api/`)

**Purpose**: FastAPI web service for programmatic access to research capabilities

```
src/api/
├── __init__.py               # API module initialization
├── main.py                   # FastAPI application setup and configuration
├── routers/                  # API route handlers organized by functionality
│   ├── __init__.py
│   ├── auth.py              # Authentication and authorization endpoints
│   ├── research.py          # Research operation endpoints (start, status, results)
│   └── reports.py           # Report management endpoints (list, download, export)
└── middleware/               # HTTP middleware for cross-cutting concerns
    ├── __init__.py
    ├── auth.py              # Authentication middleware and token validation
    ├── cors.py              # CORS configuration for web client access
    └── logging.py           # Request/response logging and monitoring
```

**Key Features**:

- RESTful API endpoints for all CLI functionality
- Authentication and authorization system
- Real-time research status updates
- File upload/download for reports

### Workflow Engine (`src/workflows/`)

**Purpose**: LangGraph-based orchestration of multi-agent research processes

```
src/workflows/
├── __init__.py               # Workflow module exports
├── due_diligence.py         # Main due diligence workflow coordination
├── minimal.py               # Simplified workflow for demo/testing
├── nodes/                    # Individual workflow nodes (steps)
│   ├── __init__.py
│   ├── planner.py           # Research planning and scope determination
│   ├── researcher.py        # Core research execution coordination
│   └── synthesizer.py       # Result synthesis and report generation
└── utils/                    # Workflow utility functions
    ├── __init__.py
    ├── state.py             # Workflow state management
    └── tools.py             # Tool integrations (EXA search, web scraping)
```

**Key Features**:

- LangGraph state machine for complex workflow orchestration
- Parallel agent execution with result synthesis
- Error handling and retry mechanisms
- Configurable workflow parameters

### Configuration (`src/config/`)

**Purpose**: Centralized configuration management and settings

```
src/config/
├── __init__.py               # Configuration module exports
├── settings.py              # Main settings class with environment variable loading
└── prompts.py               # Agent prompts and templates
```

**Key Features**:

- Environment-based configuration
- API key management and validation
- Default parameters for research operations
- Prompt templates for consistent agent behavior

### Core Utilities (`src/core/`)

**Purpose**: Shared utilities and base classes used across the system

```
src/core/
├── __init__.py               # Core module exports
├── types.py                 # Type definitions and data models
├── exceptions.py            # Custom exception classes
└── logging.py               # Logging configuration and utilities
```

**Key Features**:

- Consistent type definitions across modules
- Structured error handling
- Centralized logging configuration

## Documentation (`docs/`)

```
docs/
├── README.md                 # Documentation overview and navigation
├── getting-started.md        # Quick start guide for new users
├── design/                   # Architecture and design documentation
│   ├── architecture.md      # High-level system architecture
│   ├── cli-design.md        # CLI design principles and patterns
│   └── workflow-design.md   # LangGraph workflow architecture
├── guides/                   # User guides for different features
│   ├── research-guide.md    # How to conduct research effectively
│   ├── configuration.md     # Configuration and setup guide
│   └── reports.md           # Report management and export guide
└── api/                      # API documentation
    ├── overview.md          # API overview and authentication
    ├── endpoints.md         # Endpoint reference
    └── examples.md          # Usage examples and code samples
```

## Test Suite (`tests/`)

```
tests/
├── __init__.py               # Test package initialization
├── conftest.py              # Pytest configuration and fixtures
├── test_cli/                # CLI component tests
│   ├── test_commands.py     # Command functionality tests
│   └── test_ui.py           # UI component tests
├── test_agents/             # Agent system tests
│   ├── test_base.py         # Base agent functionality
│   └── test_financial.py   # Financial agent specific tests
├── test_api/                # API endpoint tests
│   ├── test_auth.py         # Authentication tests
│   └── test_research.py    # Research endpoint tests
└── test_workflows/          # Workflow integration tests
    ├── test_due_diligence.py # Main workflow tests
    └── test_nodes.py        # Individual node tests
```

## Development Scripts (`scripts/`)

```
scripts/
├── setup.py                 # Development environment setup
├── test.py                  # Test runner script
└── deploy.py               # Deployment automation
```

## Key Integration Points

### CLI → Workflow Integration

- `src/cli/commands/research.py` imports and executes `src/workflows/due_diligence.py`
- Progress tracking bridges CLI UI with workflow state updates
- Session persistence allows resuming long-running research tasks

### Agent → Workflow Integration

- Agents are instantiated and orchestrated by workflow nodes
- `src/workflows/nodes/researcher.py` coordinates multiple agents
- Results are aggregated in `src/workflows/nodes/synthesizer.py`

### API → Core Integration

- API endpoints expose CLI functionality programmatically
- Shared configuration and models ensure consistency
- Real-time status updates bridge async workflows with HTTP responses

## Entry Points

1. **Installed CLI**: `dd` command → `src/cli/main.py:app()` (via pyproject.toml console script)
2. **Development CLI**: `python -m src.cli.main` → Direct module execution for development
3. **API Server**: `due-diligence` command → `src/api/main.py` (via pyproject.toml console script)
4. **Direct Import**: Python modules can import workflows directly

### CLI Entry Point Details

**Primary CLI Access**:
- **Installed**: `dd [command]` - Main CLI after `pip install -e .`
- **Development**: `python -m src.cli.main [command]` - No installation required
- **UV Development**: `uv run python -m src.cli.main [command]` - Managed environment

## Data Flow

1. User initiates research via CLI or API
2. Configuration loaded from `src/config/settings.py`
3. Workflow orchestrated via `src/workflows/due_diligence.py`
4. Multiple agents execute in parallel via `src/agents/`
5. Results synthesized and formatted
6. Reports saved to `reports/` directory
7. Session data persisted to `sessions/` directory

This architecture provides a modular, scalable system for automated due diligence research with multiple interfaces (CLI, API) and robust workflow orchestration.
