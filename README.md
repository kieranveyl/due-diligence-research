# Due Diligence CLI - Multi-Agent AI Research Tool

A modern command-line interface for comprehensive due diligence research using specialized AI agents. Built with LangGraph and featuring an intuitive CLI for professional research workflows.

## 🚀 Features

- **🔍 Multi-Agent Research**: Specialized AI agents for financial, legal, OSINT, and verification analysis
- **🖥️ Modern CLI**: Beautiful command-line interface with real-time progress tracking
- **📊 Interactive & Automated**: Support for both interactive research and automation scripts
- **📝 Professional Reports**: Generate comprehensive reports in markdown, JSON, and PDF formats
- **⚙️ Flexible Configuration**: Customizable research parameters and output settings
- **💾 Session Management**: Save and resume long-running research sessions
- **🎯 Smart Entity Detection**: Automatically optimize research approach for companies vs. individuals

## 📋 Requirements

- **Python 3.11+**
- **API Keys Required**: OpenAI, Exa
- **API Keys Optional**: Anthropic, LangSmith

## 🚀 Quick Start

### 1. Installation

```bash
# Install with uv (recommended)
git clone <repository-url>
cd due-diligence-exa
uv sync

# Or install with pip
pip install -e .
```

### 2. Configure API Keys

```bash
# Option 1: Interactive setup (recommended)
dd config set

# Option 2: Environment variables
export OPENAI_API_KEY="your_openai_key_here"
export EXA_API_KEY="your_exa_key_here"
```

### 3. Verify Setup

```bash
# Check configuration
dd config show

# Validate API keys
dd config validate

# Check system health
dd health
```

### 4. Run Your First Research

```bash
# Interactive research (recommended for first-time users)
dd research run "Tesla Inc"

# Quick non-interactive research
dd research run "Apple Inc" --scope financial --no-interactive

# Custom output location
dd research run "Microsoft Corp" --output ./my-reports/msft-analysis.md
```

## 🎯 Key Commands

### Research Commands
```bash
# Basic research
dd research run "Tesla Inc"

# Advanced research with options
dd research run "Apple Inc" \
  --scope financial,legal,osint \
  --confidence-threshold 0.9 \
  --output ./reports/apple.md

# Check research status
dd research status

# Resume interrupted research
dd research run --resume abc12345
```

### Configuration Management
```bash
dd config show              # View current settings
dd config set               # Interactive configuration
dd config validate          # Validate setup
dd config reset             # Reset to defaults
```

### Reports Management
```bash
dd reports list             # List all reports
dd reports show report.md   # View report content
dd reports export report.md --format pdf  # Export to PDF
dd reports cleanup --older-than 30        # Clean old reports
```

## 📊 Example Workflows

### Investment Research
```bash
dd research run "Potential Investment Target" \
  --scope financial,verification \
  --confidence-threshold 0.9 \
  --save-session
```

### Legal Due Diligence
```bash
dd research run "Acquisition Target" \
  --scope legal,verification \
  --max-sources 100 \
  --timeout 1800
```

### Quick Screening
```bash
dd research run "Startup Company" \
  --scope financial,osint \
  --no-interactive \
  --timeout 600
```

## 🏗️ CLI Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Due Diligence CLI                           │
├─────────────────────────────────────────────────────────────────┤
│  CLI Interface (Click + Rich)                                  │
│  ├── Research Commands                                          │
│  ├── Configuration Management                                   │
│  ├── Report Management                                          │
│  └── System Health Monitoring                                  │
├─────────────────────────────────────────────────────────────────┤
│  Multi-Agent Research Engine                                   │
│  ├── 🏦 Financial Agent (Investment Analysis)                   │
│  ├── ⚖️ Legal Agent (Compliance & Litigation)                   │
│  ├── 🔍 OSINT Agent (Open Source Intelligence)                  │
│  └── ✅ Verification Agent (Cross-Validation)                   │
├─────────────────────────────────────────────────────────────────┤
│  External APIs & Data Sources                                  │
│  ├── OpenAI (Primary AI Analysis)                              │
│  ├── Exa (Web Search & Data Collection)                        │
│  ├── Anthropic (Secondary AI Verification)                     │
│  └── LangSmith (Monitoring & Observability)                    │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
due-diligence-exa/
├── src/
│   ├── cli/                    # Command-line interface
│   │   ├── main.py             # CLI entry point
│   │   ├── commands/           # Command implementations
│   │   │   ├── research.py     # Research commands
│   │   │   ├── config.py       # Configuration management
│   │   │   ├── reports.py      # Report management
│   │   │   └── utils.py        # Utility functions
│   │   ├── models/             # CLI data models
│   │   └── ui/                 # Rich UI components
│   ├── agents/                 # Multi-agent implementations
│   ├── api/                    # FastAPI backend (optional)
│   ├── workflows/              # LangGraph research workflows
│   ├── state/                  # State management
│   └── tools/                  # External API integrations
├── docs/                       # Comprehensive documentation
│   ├── user-guide/             # User guides and tutorials
│   ├── design/                 # Architecture documentation
│   └── examples/               # Usage examples
├── tests/                      # Test suite
└── reports/                    # Generated research reports
```

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[User Guide](./docs/user-guide/)** - Complete guides for using the CLI
  - [Getting Started](./docs/user-guide/getting-started.md) - Installation and setup
  - [Research Guide](./docs/user-guide/research-guide.md) - Conducting research
  - [Configuration](./docs/user-guide/configuration.md) - Customizing settings
  - [Reports Management](./docs/user-guide/reports.md) - Managing reports
  - [CLI Reference](./docs/user-guide/cli-reference.md) - Complete command reference

- **[Design Documentation](./docs/design/)** - Architecture and design
  - [System Overview](./docs/design/overview.md) - High-level architecture

- **[Examples](./docs/examples/)** - Practical usage examples
  - [Quick Start Examples](./docs/examples/quick-start.md) - Get started fast

## 🔧 Configuration Options

The CLI supports extensive configuration through:

### Configuration File
- Location: `~/.config/due-diligence/config.json`
- Interactive setup: `dd config set`
- View settings: `dd config show`

### Key Settings
- **Research Scope**: Default research areas (financial, legal, osint, verification)
- **Confidence Threshold**: Minimum confidence for findings (0.7-1.0)
- **Output Format**: Default report format (markdown, json, pdf)
- **Timeout**: Research duration limits
- **Model Selection**: Choose AI models for analysis

### Environment Variables
```bash
# Required API Keys
OPENAI_API_KEY=your_openai_key
EXA_API_KEY=your_exa_key

# Optional API Keys
ANTHROPIC_API_KEY=your_anthropic_key
LANGSMITH_API_KEY=your_langsmith_key

# Configuration
DD_CONFIG_DIR=/custom/config/path
DD_REPORTS_DIR=/custom/reports/path
```

## 🚀 Advanced Usage

### Automation Scripts
```bash
#!/bin/bash
# Batch research script
entities=("Tesla Inc" "Apple Inc" "Microsoft Corp")
for entity in "${entities[@]}"; do
    dd research run "$entity" --scope financial --no-interactive
done
```

### Custom Workflows
```bash
# High-confidence investment analysis
dd research run "Investment Target" \
  --scope financial,verification \
  --confidence-threshold 0.95 \
  --max-sources 100 \
  --save-session

# Quick compliance check
dd research run "Business Partner" \
  --scope legal,osint \
  --timeout 600 \
  --no-interactive
```

## 🧪 Testing

```bash
# Install development dependencies
uv sync --dev

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Test CLI commands
dd health
dd config validate
```

## 🆘 Getting Help

### Documentation
- **[Getting Started Guide](./docs/user-guide/getting-started.md)** - New user setup
- **[CLI Reference](./docs/user-guide/cli-reference.md)** - Complete command documentation
- **[Examples](./docs/examples/quick-start.md)** - Practical usage examples

### CLI Help
```bash
dd --help                    # General help
dd research run --help       # Command-specific help
dd config --help            # Configuration help
```

### System Diagnostics
```bash
dd health                   # System health check
dd config validate          # Validate configuration
dd config show              # View current settings
```

## 🔄 What's Next?

After getting started:

1. **Read the [Research Guide](./docs/user-guide/research-guide.md)** to learn advanced techniques
2. **Explore [Configuration Options](./docs/user-guide/configuration.md)** to customize your setup
3. **Check out [Report Management](./docs/user-guide/reports.md)** to organize your research
4. **Try [Automation Examples](./docs/examples/quick-start.md)** for workflow automation

## 🎯 Use Cases

### Investment Analysis
Perfect for investment firms, VCs, and individual investors conducting due diligence on potential investments.

### M&A Due Diligence
Comprehensive research for mergers and acquisitions, covering financial, legal, and operational aspects.

### Background Checks
Professional background verification for hiring, partnerships, and business relationships.

### Compliance Monitoring
Ongoing monitoring of business partners, suppliers, and other stakeholders for compliance risks.

### Competitive Intelligence
Research competitors, market dynamics, and industry trends for strategic planning.

---

**🔍 Built for professionals who need reliable, comprehensive, and efficient due diligence research.**