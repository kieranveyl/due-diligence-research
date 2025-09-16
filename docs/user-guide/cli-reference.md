# CLI Reference

Complete reference documentation for all Due Diligence CLI commands and options.

## 📋 Global Options

These options are available for all commands:

| Option | Description |
|--------|-------------|
| `--help` | Show help message and exit |
| `--version` | Show version information |

## 🔬 Research Commands

### `dd research [ENTITY_NAME]`

Conduct due diligence research on an entity.

#### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ENTITY_NAME` | string | Yes | Name of entity to research |

#### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--scope` | | string | interactive | Comma-separated research areas |
| `--output` | `-o` | path | auto | Custom output path for report |
| `--format` | | choice | markdown | Output format (markdown, json, pdf) |
| `--no-interactive` | | flag | false | Skip interactive prompts |
| `--confidence-threshold` | | float | 0.8 | Minimum confidence threshold |
| `--max-sources` | | int | 50 | Maximum sources to use |
| `--timeout` | | int | 300 | Research timeout in seconds |
| `--model` | | string | config | Override default LLM model |
| `--parallel-tasks` | | int | config | Number of parallel tasks |
| `--save-session` | | flag | false | Save session for later review |
| `--resume` | | string | | Resume previous session by ID |

#### Scope Values

| Scope | Description |
|-------|-------------|
| `financial` | Financial health, revenue, investments, risks |
| `legal` | Legal compliance, litigation, regulatory status |
| `osint` | Open source intelligence, public records, news |
| `verification` | Cross-verification, fact-checking, confidence |

#### Examples

```bash
# Basic interactive research
dd research "Tesla Inc"

# Non-interactive with specific scope
dd research "Apple Inc" --scope financial,legal --no-interactive

# Custom output and high confidence
dd research "Microsoft Corp" --output ./reports/msft.md --confidence-threshold 0.9

# Quick research with timeout
dd research "Startup Inc" --timeout 600 --max-sources 25

# Resume previous session
dd research --resume abc12345
```

### `dd research status [SESSION_ID]`

Check status of research sessions.

#### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `SESSION_ID` | string | No | Specific session ID to check |

#### Examples

```bash
# List recent sessions
dd research status

# Check specific session
dd research status abc12345
```

## ⚙️ Configuration Commands

### `dd config show`

Display current configuration settings.

#### Examples

```bash
dd config show
```

### `dd config set [SETTING] [VALUE]`

Set configuration values.

#### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `SETTING` | string | No | Setting name to configure |
| `VALUE` | string | No | New value for setting |

#### Available Settings

| Setting | Type | Description |
|---------|------|-------------|
| `default_output_dir` | path | Default reports directory |
| `default_format` | choice | Default output format |
| `default_scope` | list | Default research areas |
| `confidence_threshold` | float | Minimum confidence threshold |
| `max_sources` | int | Maximum sources per research |
| `timeout` | int | Research timeout in seconds |
| `model` | string | Default LLM model |
| `parallel_tasks` | int | Max parallel tasks |
| `auto_validate_keys` | bool | Auto-validate API keys |

#### Examples

```bash
# Interactive configuration
dd config set

# Set specific value
dd config set default_output_dir "./my-reports"

# Set multiple scope values
dd config set default_scope "financial,legal,osint"

# Set numeric values
dd config set confidence_threshold 0.9
dd config set max_sources 75
dd config set timeout 1800
```

### `dd config reset`

Reset configuration to defaults.

#### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--yes` | `-y` | Skip confirmation prompt |

#### Examples

```bash
# Interactive reset
dd config reset

# Force reset without confirmation
dd config reset --yes
```

### `dd config validate`

Validate current configuration and API keys.

#### Examples

```bash
dd config validate
```

### `dd config export`

Export configuration to file.

#### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--output` | `-o` | path | Output file path |

#### Examples

```bash
# Export with default name
dd config export

# Export to specific file
dd config export --output my-config.json
```

### `dd config import [CONFIG_FILE]`

Import configuration from file.

#### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `CONFIG_FILE` | path | Yes | Configuration file to import |

#### Options

| Option | Description |
|--------|-------------|
| `--merge` | Merge with existing config instead of replacing |

#### Examples

```bash
# Replace entire configuration
dd config import my-config.json

# Merge with existing configuration
dd config import my-config.json --merge
```

## 📊 Reports Commands

### `dd reports list`

List all available reports.

#### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--dir` | `-d` | path | config | Reports directory to scan |
| `--limit` | `-l` | int | 20 | Maximum number of reports to show |

#### Examples

```bash
# List reports in default directory
dd reports list

# List reports in specific directory
dd reports list --dir ./my-reports

# Show more reports
dd reports list --limit 50
```

### `dd reports show [REPORT_NAME]`

Display report content.

#### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `REPORT_NAME` | string | Yes | Report filename or session ID |

#### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--dir` | `-d` | path | Reports directory |
| `--lines` | `-n` | int | Number of lines to show |

#### Examples

```bash
# Show full report
dd reports show tesla-analysis.md

# Show report by session ID
dd reports show abc12345

# Show first 50 lines
dd reports show tesla-analysis.md --lines 50

# Show report from specific directory
dd reports show tesla-analysis.md --dir ./my-reports
```

### `dd reports export [REPORT_NAME]`

Export report to different format.

#### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `REPORT_NAME` | string | Yes | Report filename or session ID |

#### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--format` | `-f` | choice | pdf | Output format (pdf, json, markdown) |
| `--output` | `-o` | path | auto | Output file path |
| `--dir` | `-d` | path | config | Reports directory |

#### Examples

```bash
# Export to PDF
dd reports export tesla-analysis.md --format pdf

# Export with custom output path
dd reports export tesla-analysis.md --format json --output ./exports/tesla.json

# Export by session ID
dd reports export abc12345 --format pdf
```

### `dd reports cleanup`

Clean up old reports.

#### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--dir` | path | config | Reports directory |
| `--older-than` | int | 30 | Delete reports older than N days |
| `--dry-run` | flag | false | Show what would be deleted without deleting |
| `--yes` | flag | false | Skip confirmation prompts |

#### Examples

```bash
# Clean up reports older than 30 days (interactive)
dd reports cleanup

# Clean up reports older than 7 days
dd reports cleanup --older-than 7

# See what would be cleaned up without deleting
dd reports cleanup --dry-run

# Clean up without confirmation
dd reports cleanup --older-than 30 --yes
```

### `dd reports summary`

Show reports summary statistics.

#### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--dir` | `-d` | path | Reports directory |

#### Examples

```bash
# Show summary for default directory
dd reports summary

# Show summary for specific directory
dd reports summary --dir ./my-reports
```

## 🏥 System Commands

### `dd health`

Check system health and API connectivity.

#### Examples

```bash
dd health
```

### `dd version`

Show version information.

#### Examples

```bash
dd version
```

## 🔧 Environment Variables

These environment variables affect CLI behavior:

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key for AI analysis |
| `EXA_API_KEY` | Exa API key for web search |
| `ANTHROPIC_API_KEY` | Anthropic API key (optional) |
| `LANGSMITH_API_KEY` | LangSmith API key (optional) |
| `DD_CONFIG_DIR` | Custom configuration directory |
| `DD_REPORTS_DIR` | Default reports directory |

## 📁 File Locations

### Configuration

- **Linux/macOS**: `~/.config/due-diligence/config.json`
- **Windows**: `%APPDATA%\due-diligence\config.json`

### Reports

- **Default**: `./reports/` (current directory)
- **Configurable**: Set via `default_output_dir` setting

### Session Data

- **Linux/macOS**: `~/.config/due-diligence/sessions/`
- **Windows**: `%APPDATA%\due-diligence\sessions\`

## 🚨 Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | General error |
| 2 | Configuration error |
| 3 | API key error |
| 4 | Network error |
| 5 | File/permission error |

## 💡 Tips and Tricks

### Command Aliases

You can create shell aliases for common commands:

```bash
# Add to your .bashrc or .zshrc
alias ddr="dd research"
alias ddc="dd config"
alias ddl="dd reports list"
```

### Output Redirection

```bash
# Save command output to file
dd reports list > reports-inventory.txt

# Append to log file
dd research "Entity" 2>&1 | tee -a research.log
```

### Scripting Integration

```bash
#!/bin/bash
# Automated research script

ENTITY="$1"
DATE=$(date +%Y%m%d)
OUTPUT_DIR="./daily-research/$DATE"

mkdir -p "$OUTPUT_DIR"

dd research "$ENTITY" \
  --no-interactive \
  --scope financial,legal \
  --output "$OUTPUT_DIR/$ENTITY-analysis.md" \
  --save-session
```

### Tab Completion

The CLI supports tab completion for commands and options. To enable:

```bash
# For bash
eval "$(_DD_COMPLETE=bash_source dd)" >> ~/.bashrc

# For zsh
eval "$(_DD_COMPLETE=zsh_source dd)" >> ~/.zshrc
```

## 🔗 Related Documentation

- **[Getting Started](./getting-started.md)** - Initial setup and first steps
- **[Research Guide](./research-guide.md)** - Comprehensive research techniques
- **[Configuration Guide](./configuration.md)** - Detailed configuration options
- **[Examples](../examples/quick-start.md)** - Practical usage examples