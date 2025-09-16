# Research Guide

This guide covers comprehensive due diligence research using the CLI tool. Learn how to conduct thorough, professional-grade investigations using AI agents.

## 🎯 Understanding Due Diligence Research

The Due Diligence CLI uses specialized AI agents to investigate entities across multiple dimensions:

- **🏦 Financial Agent** - Financial health, revenue, investments, risks
- **⚖️ Legal Agent** - Legal issues, compliance, litigation, regulatory status
- **🔍 OSINT Agent** - Open source intelligence, public records, news analysis
- **✅ Verification Agent** - Cross-verification, fact-checking, confidence assessment

## 🚀 Basic Research Workflow

### 1. Start Interactive Research

```bash
dd research "Target Entity Name"
```

The CLI will:
1. **Auto-detect entity type** (company, person, organization)
2. **Confirm analysis approach** with you
3. **Let you select research scope** interactively
4. **Ask for custom report location** (or use defaults)
5. **Execute multi-agent research** with real-time progress
6. **Generate comprehensive report**

### 2. Entity Type Detection

The system automatically detects:

- **Companies**: "Tesla Inc", "Apple Corp", "Microsoft Corporation"
- **Individuals**: "John Smith", "CEO Jane Doe"
- **Organizations**: "Department of Energy", "World Health Organization"

Each type gets optimized research approaches and agent configurations.

## 🎛️ Research Scope Configuration

### Available Research Areas

| Scope | Description | Best For |
|-------|-------------|----------|
| `financial` | Financial analysis, revenue, investments | Investment decisions, M&A |
| `legal` | Legal compliance, litigation, regulatory | Risk assessment, compliance |
| `osint` | Open source intelligence, public data | Background checks, investigations |
| `verification` | Cross-verification, fact-checking | High-stakes decisions |

### Interactive Scope Selection

When running interactively, you'll see:

```
🔍 Research Scope Selection
Use ↑↓ to navigate, space to toggle, enter to confirm:

→ ☑ financial: Financial health and investment analysis
  ☐ legal: Legal compliance and litigation analysis
  ☐ osint: Open source intelligence gathering
  ☐ verification: Cross-verification and fact-checking
```

### Command Line Scope

```bash
# Single scope
dd research "Tesla Inc" --scope financial

# Multiple scopes
dd research "Tesla Inc" --scope financial,legal,osint

# All scopes
dd research "Tesla Inc" --scope financial,legal,osint,verification
```

## 📊 Research Parameters

### Confidence Threshold

Controls minimum confidence level for findings:

```bash
# High confidence only (90%+)
dd research "Tesla Inc" --confidence-threshold 0.9

# Accept medium confidence (70%+)
dd research "Tesla Inc" --confidence-threshold 0.7
```

### Source Limits

Control research depth:

```bash
# Quick research (fewer sources)
dd research "Tesla Inc" --max-sources 25

# Deep research (more sources)
dd research "Tesla Inc" --max-sources 100
```

### Timeout Controls

Manage research duration:

```bash
# Quick research (5 minutes)
dd research "Tesla Inc" --timeout 300

# Extended research (30 minutes)
dd research "Tesla Inc" --timeout 1800
```

## 🔄 Advanced Research Patterns

### Non-Interactive Research

For automation and scripting:

```bash
dd research "Apple Inc" \
  --scope financial,legal \
  --no-interactive \
  --output ./reports/apple-$(date +%Y%m%d).md \
  --confidence-threshold 0.8 \
  --max-sources 75
```

### Custom Output Paths

```bash
# Specific file
dd research "Tesla Inc" --output ./reports/tesla-analysis.md

# Dynamic naming
dd research "Tesla Inc" --output "./reports/tesla-$(date +%Y%m%d).md"

# Different format
dd research "Tesla Inc" --output ./reports/tesla.json --format json
```

### Session Management

For long-running research:

```bash
# Save session for later review
dd research "Complex Entity" --save-session

# Resume interrupted research
dd research --resume abc12345
```

## 📈 Understanding Progress

### Real-Time Progress Display

During research, you'll see:

```
🔍 Research Status
📋 Phase: Research Execution
⏱️  Elapsed: 45s
📊 Progress: 2/4 tasks completed

🤖 Agent Status
💰 Financial     ████████████ 100%  Complete (confidence: 87.2%)
⚖️  Legal        █████████░░░ 75%   Processing...
🔍 Osint         ██████░░░░░░ 50%   Processing...
✅ Verification  ░░░░░░░░░░░░ 0%    Pending...
```

### Progress Phases

1. **Initialization** - Setting up agents and workflows
2. **Research Execution** - Agents gathering and analyzing data
3. **Synthesis** - Combining findings and generating report

## 📋 Report Structure

### Generated Report Sections

Each report includes:

**Executive Summary**
- Overall confidence assessment
- Key findings summary
- Risk highlights
- Recommendation summary

**Detailed Analysis by Agent**
- Financial analysis findings
- Legal compliance assessment
- OSINT intelligence gathered
- Verification cross-checks

**Sources and Citations**
- All sources used
- Source reliability scores
- Date and method of collection

**Confidence Metrics**
- Per-agent confidence scores
- Overall confidence rating
- Uncertainty indicators

### Report Formats

```bash
# Markdown (default)
dd research "Tesla Inc" --format markdown

# JSON for programmatic use
dd research "Tesla Inc" --format json

# PDF for presentations (requires additional setup)
dd research "Tesla Inc" --format pdf
```

## 🎯 Research Best Practices

### 1. Entity Name Preparation

**Good Entity Names:**
- "Tesla Inc" (official company name)
- "John Smith, CEO of Acme Corp" (with context)
- "U.S. Department of Energy" (full official name)

**Avoid:**
- "TSLA" (ticker symbols without context)
- "John" (too generic without context)
- "That company we talked about" (vague references)

### 2. Scope Selection Strategy

**For Investment Decisions:**
```bash
dd research "Target Company" --scope financial,legal,verification
```

**For Hiring/Partnership:**
```bash
dd research "Potential Partner" --scope osint,legal,verification
```

**For Comprehensive Analysis:**
```bash
dd research "Subject Entity" --scope financial,legal,osint,verification
```

### 3. Managing Research Time

**Quick Overview (5-10 minutes):**
```bash
dd research "Entity" --scope financial --max-sources 25 --timeout 600
```

**Standard Research (15-30 minutes):**
```bash
dd research "Entity" --scope financial,legal --max-sources 50 --timeout 1800
```

**Deep Investigation (45+ minutes):**
```bash
dd research "Entity" --scope financial,legal,osint,verification --max-sources 100 --timeout 3600
```

## 🔍 Interpreting Results

### Confidence Scores

- **90%+** - High confidence, strong evidence
- **80-89%** - Good confidence, solid findings
- **70-79%** - Moderate confidence, some uncertainty
- **60-69%** - Low confidence, limited evidence
- **<60%** - Very low confidence, insufficient data

### Risk Indicators

Watch for:
- **Financial** - Declining revenue, high debt, cash flow issues
- **Legal** - Active litigation, regulatory violations, compliance gaps
- **OSINT** - Negative news, reputation issues, public controversies
- **Verification** - Inconsistent information, conflicting sources

### Decision Making

Use confidence scores and risk indicators to:
1. **High confidence + Low risk** → Proceed with confidence
2. **High confidence + High risk** → Proceed with caution and mitigation
3. **Low confidence + Any risk** → Gather more information before proceeding

## 🔄 Session Management

### Saving Sessions

```bash
# Automatically save important research
dd research "Critical Entity" --save-session

# Session ID will be provided (e.g., abc12345)
```

### Reviewing Sessions

```bash
# List recent sessions
dd research status

# View specific session
dd research status abc12345

# Resume incomplete session
dd research --resume abc12345
```

### Session Benefits

- **Audit Trail** - Complete record of research conducted
- **Resumability** - Continue interrupted research
- **Reproducibility** - Understand how conclusions were reached
- **Collaboration** - Share session IDs with team members

## 🚨 Troubleshooting Research

### Common Issues

**Low Confidence Scores**
- Increase `--max-sources` for more data
- Expand scope to include more research areas
- Check entity name accuracy and specificity

**Research Timeouts**
- Increase `--timeout` parameter
- Reduce `--max-sources` for faster completion
- Use `--save-session` to preserve partial progress

**No Results Found**
- Verify entity name spelling and format
- Try alternative entity names or identifiers
- Check that entity has sufficient public information

### Getting Better Results

1. **Use official entity names** when possible
2. **Include context** for common names (e.g., "John Smith, CEO of Acme Corp")
3. **Start broad, then narrow** scope based on initial findings
4. **Adjust confidence thresholds** based on decision criticality
5. **Save sessions** for important research that might need review

## 📚 Next Steps

- **[Configuration Guide](./configuration.md)** - Customize your research settings
- **[Reports Management](./reports.md)** - Managing and exporting reports
- **[CLI Reference](./cli-reference.md)** - Complete command documentation
- **[Advanced Examples](../examples/advanced.md)** - Complex research scenarios