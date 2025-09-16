# Configuration Guide

This guide covers comprehensive configuration of the Due Diligence CLI, from basic setup to advanced customization.

## 🎯 Configuration Overview

The CLI uses a hierarchical configuration system:

1. **Environment Variables** (highest priority)
2. **Command Line Arguments**
3. **Configuration File** (`~/.config/due-diligence/config.json`)
4. **System Defaults** (lowest priority)

## 🚀 Quick Setup

### Interactive Configuration

The fastest way to get started:

```bash
dd config set
```

This launches an interactive setup wizard that guides you through:
- Output directory settings
- Default research scope
- Confidence thresholds
- Model preferences
- API key configuration

### Check Current Configuration

```bash
dd config show
```

Displays:
- All current settings and values
- API key status (configured/missing)
- Configuration file location

### Validate Setup

```bash
dd config validate
```

Verifies:
- All settings are valid
- API keys are configured and working
- Output directories are accessible
- System health

## 🔑 API Key Configuration

### Required API Keys

| Service | Purpose | Required |
|---------|---------|----------|
| **OpenAI** | Primary AI analysis engine | ✅ Yes |
| **Exa** | Web search and data collection | ✅ Yes |
| **Anthropic** | Secondary AI for verification | ⚪ Optional |
| **LangSmith** | Monitoring and observability | ⚪ Optional |

### Setting API Keys

#### Method 1: Interactive Setup
```bash
dd config set
# Follow prompts for API key input
```

#### Method 2: Environment Variables (Recommended)
```bash
export OPENAI_API_KEY="sk-..."
export EXA_API_KEY="..."
export ANTHROPIC_API_KEY="sk-ant-..."  # Optional
export LANGSMITH_API_KEY="..."         # Optional
```

Add to your shell profile (`.bashrc`, `.zshrc`, etc.) for persistence.

#### Method 3: Direct Configuration
```bash
dd config set openai_api_key "sk-..."
dd config set exa_api_key "..."
```

### API Key Security

**Best Practices:**
- Use environment variables for production
- Never commit API keys to version control
- Rotate keys regularly
- Use least-privilege API key permissions

**File Permissions:**
The configuration file is automatically secured with `600` permissions (owner read/write only).

## ⚙️ Research Settings

### Default Research Scope

Configure which research areas are included by default:

```bash
# Set multiple scopes
dd config set default_scope "financial,legal,osint"

# Set single scope
dd config set default_scope "financial"

# Include all scopes
dd config set default_scope "financial,legal,osint,verification"
```

**Available Scopes:**
- `financial` - Financial analysis and investment research
- `legal` - Legal compliance and litigation analysis
- `osint` - Open source intelligence gathering
- `verification` - Cross-verification and fact-checking

### Confidence Threshold

Set the minimum confidence level for accepting findings:

```bash
# High confidence (90%+)
dd config set confidence_threshold 0.9

# Balanced confidence (80%)
dd config set confidence_threshold 0.8

# Lower threshold for broader results (70%)
dd config set confidence_threshold 0.7
```

**Guidelines:**
- **0.9+** - Critical decisions, high-stakes analysis
- **0.8-0.89** - Standard business decisions
- **0.7-0.79** - Preliminary research, broader scope
- **<0.7** - Exploratory research only

### Source and Timeout Limits

Control research depth and duration:

```bash
# Quick research settings
dd config set max_sources 25
dd config set timeout 300     # 5 minutes

# Standard settings
dd config set max_sources 50
dd config set timeout 900     # 15 minutes

# Deep research settings
dd config set max_sources 100
dd config set timeout 1800    # 30 minutes
```

## 📁 Output Configuration

### Default Output Directory

```bash
# Current directory
dd config set default_output_dir "./reports"

# Absolute path
dd config set default_output_dir "/home/user/due-diligence/reports"

# User home directory
dd config set default_output_dir "~/due-diligence-reports"
```

The directory will be created automatically if it doesn't exist.

### Default Output Format

```bash
# Markdown (default, best for reading)
dd config set default_format "markdown"

# JSON (for programmatic processing)
dd config set default_format "json"

# PDF (for presentations, requires additional setup)
dd config set default_format "pdf"
```

## 🤖 Model Configuration

### Primary Language Model

```bash
# OpenAI models
dd config set model "gpt-4o-mini"       # Fast, cost-effective
dd config set model "gpt-4o"            # Higher quality
dd config set model "gpt-4-turbo"       # Legacy option

# Anthropic models (if configured)
dd config set model "claude-3-haiku"    # Fast option
dd config set model "claude-3-sonnet"   # Balanced option
```

### Parallel Processing

Control concurrent research operations:

```bash
# Conservative (lower resource usage)
dd config set parallel_tasks 2

# Balanced (default)
dd config set parallel_tasks 3

# Aggressive (faster but more resource intensive)
dd config set parallel_tasks 5
```

**Considerations:**
- More parallel tasks = faster research but higher API costs
- Limited by API rate limits
- Consider system resources (CPU, memory)

## 🔧 Advanced Configuration

### Auto-Validation

Control automatic API key validation:

```bash
# Enable automatic validation (default)
dd config set auto_validate_keys true

# Disable for faster startup
dd config set auto_validate_keys false
```

### Custom Configuration Directory

Override the default configuration location:

```bash
# Set custom directory
export DD_CONFIG_DIR="/custom/path/config"

# Then run CLI commands normally
dd config show
```

## 📄 Configuration File Format

The configuration is stored as JSON:

```json
{
  "default_output_dir": "./reports",
  "default_format": "markdown",
  "default_scope": [
    "financial",
    "legal",
    "osint",
    "verification"
  ],
  "confidence_threshold": 0.8,
  "max_sources": 50,
  "timeout": 300,
  "model": "gpt-4o-mini",
  "parallel_tasks": 3,
  "auto_validate_keys": true
}
```

### Direct File Editing

You can edit the configuration file directly:

```bash
# Find configuration file location
dd config show | grep "Configuration file"

# Edit with your preferred editor
nano ~/.config/due-diligence/config.json
```

## 🔄 Configuration Management

### Export Configuration

Save your configuration for backup or sharing:

```bash
# Export with default name
dd config export

# Export to specific file
dd config export --output my-config.json

# Export to date-stamped file
dd config export --output "config-$(date +%Y%m%d).json"
```

### Import Configuration

Restore or share configurations:

```bash
# Replace entire configuration
dd config import my-config.json

# Merge with existing configuration
dd config import my-config.json --merge
```

### Reset Configuration

Return to default settings:

```bash
# Interactive reset (with confirmation)
dd config reset

# Force reset without confirmation
dd config reset --yes
```

## 🎯 Use Case Configurations

### Investment Research

```bash
dd config set default_scope "financial,verification"
dd config set confidence_threshold 0.9
dd config set max_sources 75
dd config set timeout 1200
dd config set default_output_dir "./investment-research"
```

### Legal Due Diligence

```bash
dd config set default_scope "legal,verification"
dd config set confidence_threshold 0.85
dd config set max_sources 100
dd config set timeout 1800
dd config set default_output_dir "./legal-analysis"
```

### Quick Screening

```bash
dd config set default_scope "financial,osint"
dd config set confidence_threshold 0.75
dd config set max_sources 25
dd config set timeout 600
dd config set parallel_tasks 5
```

### Comprehensive Analysis

```bash
dd config set default_scope "financial,legal,osint,verification"
dd config set confidence_threshold 0.8
dd config set max_sources 100
dd config set timeout 2400
dd config set parallel_tasks 4
```

## 📊 Environment-Specific Configurations

### Development Environment

```bash
# Fast, lightweight settings for testing
export DD_CONFIG_DIR="./dev-config"
dd config set max_sources 10
dd config set timeout 300
dd config set confidence_threshold 0.7
dd config set parallel_tasks 2
```

### Production Environment

```bash
# Robust settings for production use
dd config set confidence_threshold 0.85
dd config set max_sources 75
dd config set timeout 1800
dd config set auto_validate_keys true
dd config set default_output_dir "/production/reports"
```

### CI/CD Pipeline

```bash
# Non-interactive, reliable settings
dd config set confidence_threshold 0.8
dd config set max_sources 50
dd config set timeout 900
dd config set auto_validate_keys false  # Skip validation for speed
```

## 🚨 Troubleshooting Configuration

### Common Issues

**Configuration Not Found**
```bash
# Check file location
dd config show

# Create default configuration
dd config reset
```

**API Key Errors**
```bash
# Validate keys
dd config validate

# Re-enter keys interactively
dd config set

# Check environment variables
env | grep -E "(OPENAI|EXA|ANTHROPIC|LANGSMITH)_API_KEY"
```

**Permission Errors**
```bash
# Check configuration directory permissions
ls -la ~/.config/due-diligence/

# Fix permissions if needed
chmod 700 ~/.config/due-diligence/
chmod 600 ~/.config/due-diligence/config.json
```

**Invalid Settings**
```bash
# Validate all settings
dd config validate

# Reset to defaults
dd config reset

# Set specific setting
dd config set confidence_threshold 0.8
```

### Debug Configuration

Check effective configuration (after all overrides):

```bash
# Show current effective settings
dd config show

# Test with specific overrides
dd research "Test Entity" \
  --confidence-threshold 0.9 \
  --max-sources 25 \
  --timeout 300 \
  --dry-run  # If available
```

## 🔗 Related Documentation

- **[Getting Started](./getting-started.md)** - Initial setup and API keys
- **[Research Guide](./research-guide.md)** - Using configuration in research
- **[CLI Reference](./cli-reference.md)** - Complete configuration command reference
- **[Examples](../examples/quick-start.md)** - Configuration examples in practice