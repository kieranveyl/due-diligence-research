# Getting Started with Due Diligence CLI

Welcome to the Due Diligence CLI! This guide will walk you through installation, initial setup, and conducting your first research.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** installed on your system
- **API Keys** for required services:
  - **OpenAI API Key** (required) - For AI analysis
  - **Exa API Key** (required) - For web search and data collection
  - **Anthropic API Key** (optional) - For additional AI capabilities
  - **LangSmith API Key** (optional) - For monitoring and observability

## 🚀 Installation

### Option 1: Install from Package (Recommended)

```bash
pip install due-diligence-exa
```

### Option 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/example/due-diligence-exa
cd due-diligence-exa

# Install with uv (recommended)
uv sync

# Or install with pip
pip install -e .
```

### Verify Installation

```bash
dd --version
```

You should see output like:
```
🔍 Due Diligence CLI v1.0.0
Multi-Agent AI Research Tool
```

## 🔑 API Key Setup

The CLI requires API keys to function. You can set them up in several ways:

### Option 1: Interactive Configuration (Recommended)

```bash
dd config set
```

This will guide you through an interactive setup process.

### Option 2: Environment Variables

```bash
export OPENAI_API_KEY="your_openai_key_here"
export EXA_API_KEY="your_exa_key_here"
export ANTHROPIC_API_KEY="your_anthropic_key_here"  # Optional
export LANGSMITH_API_KEY="your_langsmith_key_here"  # Optional
```

### Option 3: Direct Configuration

```bash
# Set individual keys
dd config set openai_api_key "your_key_here"
dd config set exa_api_key "your_key_here"
```

## ✅ Verify Setup

Check that your configuration is correct:

```bash
dd config show
```

Ensure API key validation:

```bash
dd config validate
```

Check system health:

```bash
dd health
```

## 🔍 Your First Research

Now you're ready to conduct your first due diligence research!

### Basic Research

```bash
dd research "Tesla Inc"
```

This will:
1. **Auto-detect** that Tesla Inc is a company
2. **Ask interactively** about research scope
3. **Show real-time progress** as AI agents work
4. **Generate a report** in the default location

### Quick Non-Interactive Research

```bash
dd research "Apple Inc" --scope financial,legal --no-interactive
```

### Custom Output Location

```bash
dd research "Microsoft Corp" --output ./my-reports/microsoft-analysis.md
```

## 📊 Understanding the Output

After research completes, you'll see:

- **Executive Summary** - High-level findings and confidence scores
- **Detailed Report** - Comprehensive analysis from each agent
- **Source Citations** - All sources used in the research
- **Confidence Metrics** - Reliability scores for each finding

## 📁 Report Management

### List Your Reports

```bash
dd reports list
```

### View a Report

```bash
dd reports show microsoft-analysis.md
```

### Export to Different Format

```bash
dd reports export microsoft-analysis.md --format pdf
```

## ⚙️ Basic Configuration

### Set Default Output Directory

```bash
dd config set default_output_dir "./my-reports"
```

### Set Default Research Scope

```bash
dd config set default_scope "financial,legal,osint"
```

### Adjust Confidence Threshold

```bash
dd config set confidence_threshold 0.9
```

## 🎯 Next Steps

Now that you have the basics working:

1. **Read the [Research Guide](./research-guide.md)** - Learn advanced research techniques
2. **Explore [Configuration Options](./configuration.md)** - Customize your experience
3. **Check out [Examples](../examples/quick-start.md)** - See more use cases
4. **Review [CLI Reference](./cli-reference.md)** - Complete command documentation

## 🆘 Troubleshooting

### Common Issues

**API Key Errors**
```bash
dd config validate  # Check key status
dd config set       # Reset keys interactively
```

**No Reports Found**
```bash
dd config show      # Check default output directory
mkdir -p ./reports  # Create reports directory
```

**Permission Errors**
```bash
# Ensure output directory is writable
chmod 755 ./reports
```

### Getting Help

```bash
# General help
dd --help

# Command-specific help
dd research --help
dd config --help
dd reports --help

# System health check
dd health
```

## 🔄 What's Next?

You're now ready to conduct professional-grade due diligence research! The CLI will:

- **Guide you interactively** through complex research scenarios
- **Adapt to different entity types** (companies, individuals, etc.)
- **Provide rich progress feedback** during long-running analyses
- **Generate comprehensive reports** with actionable insights

Continue to the [Research Guide](./research-guide.md) to learn advanced research techniques and best practices.