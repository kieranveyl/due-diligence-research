# Quick Start Examples

Get up and running quickly with these practical examples that demonstrate core Due Diligence CLI functionality.

## 🚀 Basic Examples

### Your First Research

```bash
# Simple company research
dd research "Tesla Inc"
```

**What happens:**

1. System detects this is a company
2. Asks you to confirm the analysis approach
3. Interactive scope selection (financial, legal, OSINT, verification)
4. Real-time progress display as agents work
5. Comprehensive report generated in `./reports/`

### Quick Non-Interactive Research

```bash
# Fast research without prompts
dd research "Apple Inc" --scope financial --no-interactive
```

**Perfect for:**

- Automation scripts
- Quick financial checks
- Batch processing multiple entities

### Custom Output Location

```bash
# Save to specific location with custom name
dd research "Microsoft Corp" --output "./my-analysis/msft-$(date +%Y%m%d).md"
```

## 🎯 Scope-Specific Examples

### Financial Analysis Only

```bash
# Focus on financial health for investment decisions
dd research "NVIDIA Corp" \
  --scope financial \
  --confidence-threshold 0.9 \
  --max-sources 75 \
  --no-interactive
```

**Use cases:**

- Investment screening
- Portfolio analysis
- Financial health checks

### Legal Compliance Check

```bash
# Focus on legal and regulatory issues
dd research "Pharmaceutical Company" \
  --scope legal,verification \
  --timeout 1800 \
  --no-interactive
```

**Use cases:**

- M&A due diligence
- Compliance verification
- Risk assessment

### Comprehensive Investigation

```bash
# Full-spectrum analysis with all agents
dd research "Target Acquisition Corp" \
  --scope financial,legal,osint,verification \
  --confidence-threshold 0.8 \
  --max-sources 100 \
  --save-session

```

**Use cases:**

- Major acquisitions
- Partnership decisions
- High-stakes investments

## 👥 Individual Research Examples

### Background Check

```bash
# Research an individual (executive, partner, etc.)
dd research "John Smith, CEO of Acme Corp" \
  --scope osint,verification \
  --no-interactive
```

### Key Person Risk Assessment

```bash
# Comprehensive individual analysis
dd research "Jane Doe, CTO at TechStart Inc" \
  --scope financial,legal,osint,verification \
  --confidence-threshold 0.85
```

## 🔧 Configuration Examples

### Initial Setup

```bash
# Interactive configuration setup
dd config set

# Set specific configurations
dd config set default_output_dir "./due-diligence-reports"
dd config set default_scope "financial,legal"
dd config set confidence_threshold 0.85
```

### API Key Setup

```bash
# Check current configuration
dd config show

# Validate API keys
dd config validate

# Set API keys interactively
dd config set
```

## 📊 Reports Management Examples

### List and View Reports

```bash
# List all reports
dd reports list

# Show recent reports with more details
dd reports list --limit 50

# View a specific report
dd reports show tesla-inc-20240315.md

# View first 50 lines of a report
dd reports show tesla-inc-20240315.md --lines 50
```

### Export and Convert Reports

```bash
# Export to PDF for presentations
dd reports export tesla-inc-20240315.md --format pdf

# Export to JSON for data processing
dd reports export tesla-inc-20240315.md --format json --output ./data/tesla.json

# Export by session ID
dd reports export abc12345 --format pdf
```

### Report Cleanup

```bash
# See what would be cleaned up (dry run)
dd reports cleanup --dry-run

# Clean up reports older than 7 days
dd reports cleanup --older-than 7

# Force cleanup without confirmation
dd reports cleanup --older-than 30 --yes
```

## 🔄 Session Management Examples

### Working with Sessions

```bash
# Start research with session saving
dd research "Complex Entity Inc" --save-session

# Check session status
dd research status

# View specific session
dd research status abc12345

# Resume interrupted research
dd research --resume abc12345
```

## 🛠️ Automation Examples

### Simple Automation Script

```bash
#!/bin/bash
# simple-research.sh

ENTITY="$1"
OUTPUT_DIR="./research-$(date +%Y%m%d)"

if [ -z "$ENTITY" ]; then
    echo "Usage: $0 'Entity Name'"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

dd research "$ENTITY" \
  --scope financial,legal \
  --no-interactive \
  --output "$OUTPUT_DIR/$(echo "$ENTITY" | tr ' ' '-' | tr '[:upper:]' '[:lower:]').md" \
  --save-session

echo "Research completed. Results in: $OUTPUT_DIR"
```

**Usage:**

```bash
chmod +x simple-research.sh
./simple-research.sh "Tesla Inc"
```

### Batch Processing Script

```bash
#!/bin/bash
# batch-research.sh

ENTITIES_FILE="$1"
OUTPUT_DIR="./batch-research-$(date +%Y%m%d)"

if [ ! -f "$ENTITIES_FILE" ]; then
    echo "Usage: $0 entities.txt"
    echo "entities.txt should contain one entity name per line"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

while IFS= read -r entity; do
    if [ -n "$entity" ]; then
        echo "Researching: $entity"

        filename=$(echo "$entity" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | tr -d '[:punct:]')

        dd research "$entity" \
          --scope financial \
          --no-interactive \
          --timeout 600 \
          --output "$OUTPUT_DIR/${filename}.md" \
          --save-session

        echo "Completed: $entity"
        sleep 5  # Rate limiting
    fi
done < "$ENTITIES_FILE"

echo "Batch processing completed. Results in: $OUTPUT_DIR"
```

**Usage:**

```bash
# Create entities list
cat > entities.txt << EOF
Tesla Inc
Apple Inc
Microsoft Corp
Amazon.com Inc
EOF

chmod +x batch-research.sh
./batch-research.sh entities.txt
```

### Daily Research Automation

```bash
#!/bin/bash
# daily-research.sh - Add to cron for daily execution

DATE=$(date +%Y%m%d)
WATCHLIST="./watchlist.txt"
OUTPUT_DIR="./daily-research/$DATE"

mkdir -p "$OUTPUT_DIR"

if [ -f "$WATCHLIST" ]; then
    while IFS= read -r entity; do
        if [ -n "$entity" ]; then
            filename=$(echo "$entity" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')

            dd research "$entity" \
              --scope financial \
              --no-interactive \
              --timeout 300 \
              --max-sources 25 \
              --output "$OUTPUT_DIR/${filename}.md"
        fi
    done < "$WATCHLIST"

    # Generate summary
    dd reports summary --dir "$OUTPUT_DIR" > "$OUTPUT_DIR/summary.txt"
fi
```

**Cron setup:**

```bash
# Add to crontab (crontab -e)
0 9 * * 1-5 /path/to/daily-research.sh
```

## 💡 Advanced Examples

### High-Confidence Deep Dive

```bash
# Maximum depth analysis for critical decisions
dd research "Critical Acquisition Target" \
  --scope financial,legal,osint,verification \
  --confidence-threshold 0.95 \
  --max-sources 150 \
  --timeout 3600 \
  --save-session \
  --output "./critical-analysis/$(date +%Y%m%d)-acquisition-analysis.md"
```

### Competitive Intelligence

```bash
# Research multiple competitors quickly
for company in "Competitor A" "Competitor B" "Competitor C"; do
    dd research "$company" \
      --scope financial,osint \
      --no-interactive \
      --timeout 900 \
      --output "./competitive-intel/$(echo "$company" | tr ' ' '-').md"
done

# Generate competitive summary
dd reports summary --dir "./competitive-intel"
```

### Regulatory Compliance Batch

```bash
# Compliance check for portfolio companies
dd research "Portfolio Company 1" --scope legal,verification --no-interactive &
dd research "Portfolio Company 2" --scope legal,verification --no-interactive &
dd research "Portfolio Company 3" --scope legal,verification --no-interactive &

wait  # Wait for all background jobs to complete

echo "Compliance analysis completed for all portfolio companies"
```

## 📋 Common Patterns

### Daily Workflow

```bash
# Morning routine: Check overnight news and updates
dd config validate  # Ensure system is ready
dd research "Primary Investment" --scope osint --timeout 300 --no-interactive
dd reports list --limit 10  # Review recent research
```

### Pre-Meeting Preparation

```bash
# Quick brief before important meeting
dd research "Meeting Subject Entity" \
  --scope financial,osint \
  --timeout 600 \
  --output "./meeting-prep/$(date +%Y%m%d)-brief.md" \
  --no-interactive
```

### Investment Committee Prep

```bash
# Comprehensive analysis for investment committee
dd research "Investment Target" \
  --scope financial,legal,verification \
  --confidence-threshold 0.9 \
  --save-session \
  --output "./investment-committee/$(date +%Y%m%d)-full-analysis.md"

# Export to PDF for presentation
dd reports export "./investment-committee/$(date +%Y%m%d)-full-analysis.md" --format pdf
```

## 🚨 Troubleshooting Examples

### Debug Mode Research

```bash
# Research with maximum verbosity for troubleshooting
dd research "Problematic Entity" \
  --scope financial \
  --max-sources 10 \
  --timeout 300 \
  --save-session \
  --no-interactive 2>&1 | tee debug.log
```

### Recovery from Interrupted Research

```bash
# Check recent sessions
dd research status

# Resume the most recent session
dd research --resume $(dd research status | head -2 | tail -1 | awk '{print $1}')
```

### Configuration Backup and Restore

```bash
# Backup configuration
dd config export --output "./backups/config-$(date +%Y%m%d).json"

# Restore configuration
dd config import "./backups/config-20240315.json"
```

## 🎯 Next Steps

After trying these examples:

1. **[Research Guide](../user-guide/research-guide.md)** - Learn advanced research techniques
2. **[Configuration Guide](../user-guide/configuration.md)** - Customize your setup
3. **[CLI Reference](../user-guide/cli-reference.md)** - Complete command documentation
4. **[Advanced Examples](./advanced.md)** - Complex research scenarios
