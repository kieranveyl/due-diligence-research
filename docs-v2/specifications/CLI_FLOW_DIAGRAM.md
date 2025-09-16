# CLI User Experience Flow

## Overview
This document details the complete user experience flow for the Due Diligence CLI, including interactive elements, progress displays, and user decision points.

## Command Entry Point

```bash
$ dd research run "Generate comprehensive report on Farhad Azima's intelligence work"
```

## Flow Diagram

### Phase 1: Initialization & Query Analysis

```
┌─────────────────────────────────────────────────────────────┐
│ $ dd research run "Generate comprehensive report on..."      │
│                                                             │
│ 🔍 Analyzing query and discovering entities...             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ ████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 60% │ │
│ │ Entities found: Farhad Azima, Intelligence networks    │ │
│ │ Domains identified: Government, Intelligence, Aviation │ │
│ │ Research scope: International activities 1970-2024    │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Phase 2: Research Plan Generation

```
┌─────────────────────────────────────────────────────────────┐
│ ✅ Analysis complete. Generating research plan...          │
│                                                             │
│ 📋 Research Plan - Hierarchical View:                      │
│                                                             │
│ ├── 1. Background Research                                  │
│ │   ├── 1.1 Personal History (OSINT Agent)                 │
│ │   ├── 1.2 Business Network (Financial Agent)             │
│ │   └── 1.3 Geographic Connections (Geographic Agent)      │
│ │                                                           │
│ ├── 2. Intelligence Connections                            │
│ │   ├── 2.1 Government Contracts (Legal Agent)             │
│ │   ├── 2.2 Security Clearances (Intelligence Agent)       │
│ │   └── 2.3 Agency Relationships (OSINT Agent)            │
│ │                                                           │
│ ├── 3. Financial Networks                                   │
│ │   ├── 3.1 Corporate Structures (Financial Agent)         │
│ │   ├── 3.2 Banking Relationships (Financial Agent)        │
│ │   └── 3.3 Asset Holdings (Financial Agent)              │
│ │                                                           │
│ └── 4. Verification & Synthesis                            │
│     ├── 4.1 Cross-reference Sources (Verification Agent)   │
│     ├── 4.2 Conflict Resolution (Verification Agent)       │
│     └── 4.3 Report Generation (Report Engine)             │
│                                                             │
│ Estimated Duration: 45-60 minutes                          │
│ Agents Required: 6 specialized agents                      │
│                                                             │
│ ❓ Approve this plan? (y/n/modify): _                      │
└─────────────────────────────────────────────────────────────┘
```

### Phase 2b: Plan Modification (if user selects 'modify')

```
┌─────────────────────────────────────────────────────────────┐
│ 🛠️  Plan Modification Mode                                 │
│                                                             │
│ Enter modification request:                                 │
│ > Add deeper focus on Iran-Contra connections              │
│                                                             │
│ 🔄 Updating plan based on your request...                 │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ ████████████████████████████████████████████████ 100%  │ │
│ │ Plan updated: Added Iran-Contra investigation section   │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ 📋 Updated Research Plan:                                  │
│ [... updated hierarchical view ...]                        │
│                                                             │
│ ❓ Approve updated plan? (y/n/modify): y                   │
└─────────────────────────────────────────────────────────────┘
```

### Phase 3: Research Execution with Live Progress

```
┌─────────────────────────────────────────────────────────────┐
│ 🚀 Executing research plan...                              │
│                                                             │
│ Overall Progress: ████████████░░░░░░░░░░░░░░░░░░░░░ 65%    │
│                                                             │
│ ┌─ 1. Background Research ──────────────────────────────┐   │
│ │ ✅ 1.1 Personal History         [OSINT Agent]         │   │
│ │ ✅ 1.2 Business Network         [Financial Agent]     │   │
│ │ 🔄 1.3 Geographic Connections   [Geographic Agent]    │   │
│ │    └─ Searching property records in Virginia...       │   │
│ └────────────────────────────────────────────────────────┘   │
│                                                             │
│ ┌─ 2. Intelligence Connections ─────────────────────────┐   │
│ │ 🔄 2.1 Government Contracts     [Legal Agent]         │   │
│ │    └─ Analyzing FOIA documents from CIA...            │   │
│ │ ⏳ 2.2 Security Clearances      [Intelligence Agent]  │   │
│ │ ⏳ 2.3 Agency Relationships     [OSINT Agent]         │   │
│ └────────────────────────────────────────────────────────┘   │
│                                                             │
│ 📊 Partial Results:                                        │
│ • Found 23 business entities linked to subject             │
│ • Identified 12 government contracts (1982-1995)           │
│ • Located property holdings in 4 countries                 │
│ ⚠️  Potential conflict detected in employment timeline     │
│                                                             │
│ Session ID: dd_session_2024_001_farhad_azima               │
└─────────────────────────────────────────────────────────────┘
```

### Phase 4: Conflict Resolution (if conflicts detected)

```
┌─────────────────────────────────────────────────────────────┐
│ ⚠️  Conflicting Information Detected                       │
│                                                             │
│ 📊 Conflict Summary:                                       │
│ • Employment Timeline: Iran Air vs. Honeywell International│
│   - Source A: "Worked at Iran Air 1978-1980" (News article)│
│     Confidence: 75% | Date: 1985-03-15                     │
│   - Source B: "Honeywell contractor 1979-1981" (Court doc) │
│     Confidence: 90% | Date: 1987-11-22                     │
│                                                             │
│ • Asset Valuation: Property in Switzerland                 │
│   - Source A: "$2.3M assessment" (Tax records)             │
│     Confidence: 95% | Date: 2020-01-01                     │
│   - Source B: "$4.1M market value" (Real estate database)  │
│     Confidence: 80% | Date: 2020-03-15                     │
│                                                             │
│ 🤖 The system will include both sources in the final       │
│    report with clear attribution and confidence scores.    │
│                                                             │
│ Press Enter to continue...                                  │
└─────────────────────────────────────────────────────────────┘
```

### Phase 5: Report Generation

```
┌─────────────────────────────────────────────────────────────┐
│ 📄 Generating comprehensive report...                      │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ ████████████████████████████████████████████████ 100%  │ │
│ │ Report sections: Executive Summary ✅ Findings ✅       │ │
│ │ Citations ✅ Conflicts ✅ Appendices ✅               │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ✅ Report generated successfully!                          │
│                                                             │
│ 📁 Output file: ./reports/farhad_azima_intelligence_2024.md │
│ 📊 Statistics:                                             │
│ • Total sources: 127                                       │
│ • High confidence findings: 89%                            │
│ • Conflicts identified: 3                                  │
│ • Research duration: 47 minutes                            │
│                                                             │
│ 🔄 Convert to PDF? (y/n): _                               │
└─────────────────────────────────────────────────────────────┘
```

### Phase 6: PDF Conversion (if selected)

```
┌─────────────────────────────────────────────────────────────┐
│ 📄→📑 Converting to PDF format...                          │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ ████████████████████████████████████████████████ 100%  │ │
│ │ Processing: Markdown → HTML → PDF                      │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ✅ PDF generated successfully!                             │
│                                                             │
│ 📁 Files created:                                          │
│ • ./reports/farhad_azima_intelligence_2024.md              │
│ • ./reports/farhad_azima_intelligence_2024.pdf             │
│                                                             │
│ 🎉 Research completed successfully!                        │
│                                                             │
│ Session saved as: dd_session_2024_001_farhad_azima         │
│ Use 'dd session resume dd_session_2024_001_farhad_azima'   │
│ to continue or modify this research.                       │
└─────────────────────────────────────────────────────────────┘
```

## Session Management Commands

### List Previous Sessions

```bash
$ dd sessions list
```

```
┌─────────────────────────────────────────────────────────────┐
│ 📚 Previous Research Sessions                              │
│                                                             │
│ ID: dd_session_2024_001_farhad_azima                       │
│ └─ Report: Farhad Azima Intelligence Analysis              │
│    Status: Completed | Duration: 47m | Sources: 127        │
│    Created: 2024-01-15 14:23:10                            │
│                                                             │
│ ID: dd_session_2024_002_tesla_financial                    │
│ └─ Report: Tesla Inc Financial Due Diligence               │
│    Status: In Progress | Duration: 23m | Sources: 89       │
│    Created: 2024-01-15 16:45:33                            │
│                                                             │
│ ID: dd_session_2024_003_crypto_exchange                    │
│ └─ Report: Binance Exchange Regulatory Analysis            │
│    Status: Failed | Duration: 12m | Sources: 34            │
│    Created: 2024-01-14 09:15:44                            │
│                                                             │
│ Use 'dd session status <id>' for details                   │
│ Use 'dd session resume <id>' to continue                   │
└─────────────────────────────────────────────────────────────┘
```

### Session Status Check

```bash
$ dd session status dd_session_2024_002_tesla_financial
```

```
┌─────────────────────────────────────────────────────────────┐
│ 📊 Session Status: Tesla Inc Financial Due Diligence       │
│                                                             │
│ Session ID: dd_session_2024_002_tesla_financial             │
│ Status: In Progress (Paused)                               │
│ Created: 2024-01-15 16:45:33                               │
│ Last Updated: 2024-01-15 17:32:15                          │
│                                                             │
│ Progress: ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 60%    │
│                                                             │
│ ✅ Completed Tasks:                                        │
│ • Background Research (OSINT Agent)                        │
│ • SEC Filings Analysis (Financial Agent)                   │
│ • Market Performance Review (Financial Agent)              │
│                                                             │
│ 🔄 In Progress:                                            │
│ • Regulatory Compliance Check (Legal Agent)                │
│   └─ Analyzing EPA violations and settlements...           │
│                                                             │
│ ⏳ Pending:                                                │
│ • Verification & Cross-reference (Verification Agent)      │
│ • Report Generation (Report Engine)                        │
│                                                             │
│ 📊 Current Statistics:                                     │
│ • Sources collected: 89                                     │
│ • High confidence: 92%                                      │
│ • Conflicts detected: 1                                     │
│                                                             │
│ Use 'dd session resume dd_session_2024_002_tesla_financial'│
│ to continue this research.                                  │
└─────────────────────────────────────────────────────────────┘
```

### Session Resume

```bash
$ dd session resume dd_session_2024_002_tesla_financial
```

```
┌─────────────────────────────────────────────────────────────┐
│ 🔄 Resuming Session: Tesla Inc Financial Due Diligence     │
│                                                             │
│ 📋 Remaining Research Plan:                                │
│                                                             │
│ ├── ✅ 1. Background Research                              │
│ ├── ✅ 2. SEC Filings Analysis                            │
│ ├── ✅ 3. Market Performance Review                        │
│ ├── 🔄 4. Regulatory Compliance Check (60% complete)      │
│ ├── ⏳ 5. Verification & Cross-reference                   │
│ └── ⏳ 6. Report Generation                                │
│                                                             │
│ 📊 Session Summary:                                        │
│ • Duration so far: 47 minutes                              │
│ • Sources collected: 89                                     │
│ • Estimated remaining: 20-25 minutes                       │
│                                                             │
│ ❓ Continue with existing plan? (y/n/modify): _           │
└─────────────────────────────────────────────────────────────┘
```

## Error Scenarios

### API Rate Limiting

```
┌─────────────────────────────────────────────────────────────┐
│ ⚠️  API Rate Limit Encountered                             │
│                                                             │
│ SEC EDGAR API: Rate limit exceeded                          │
│ └─ Next request allowed in: 2m 34s                         │
│                                                             │
│ 🔄 Continuing with other data sources...                   │
│ • Yahoo Finance API: Active ✅                             │
│ • Alpha Vantage API: Active ✅                             │
│ • Financial Times: Active ✅                               │
│                                                             │
│ The system will automatically retry SEC EDGAR when the     │
│ rate limit resets. Research continues with available data. │
│                                                             │
│ Current progress: ████████████░░░░░░░░░░░░░░░░░░░░░ 55%    │
└─────────────────────────────────────────────────────────────┘
```

### Partial Agent Failure

```
┌─────────────────────────────────────────────────────────────┐
│ ⚠️  Agent Execution Warning                                │
│                                                             │
│ Legal Agent: Connection timeout to PACER database          │
│ └─ Retrying with alternative sources...                    │
│                                                             │
│ Alternative sources being used:                             │
│ • Justia Court Documents ✅                                │
│ • CourtListener Database ✅                                │
│ • State Court Records ✅                                   │
│                                                             │
│ 📊 Impact Assessment:                                      │
│ • Federal court records: Limited access                    │
│ • State court records: Full access                         │
│ • Overall completeness: ~85% (acceptable)                  │
│                                                             │
│ 🤖 Research continues with available data sources.         │
│    Final report will note any data limitations.            │
└─────────────────────────────────────────────────────────────┘
```

## Silent Mode (Non-Interactive)

For automation and scripting, the system supports silent mode:

```bash
$ dd research run --silent "Tesla Inc financial analysis"
```

```
Starting research session: dd_session_2024_004_tesla_financial
Research complete. Report generated: ./reports/tesla_financial_2024.md
Session duration: 42m | Sources: 156 | Confidence: 91%
```

Progress can be checked separately:

```bash
$ dd session status dd_session_2024_004_tesla_financial --format=json
```

## Technical Implementation Notes

### UI Framework
- **Rich**: Primary library for progress bars, tables, and formatting
- **Textual**: For more complex interactive elements (tree views, forms)
- **Click**: Command-line interface and argument parsing

### Progress Tracking
- **Event-driven updates**: Agents emit progress events via Redis streams
- **Real-time rendering**: UI updates every 100ms with new progress data
- **Hierarchical display**: Tree structure mirrors task dependencies

### Session Persistence
- **Auto-save**: Session state saved every 30 seconds
- **Crash recovery**: Automatic session restoration on CLI restart
- **Manual checkpoints**: Users can explicitly save session state

This detailed flow provides a comprehensive user experience that balances automation with user control, real-time feedback with clear decision points, and technical capability with intuitive interaction.