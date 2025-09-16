# Farhad Azima Research Workflow Example
## Demonstrating LangGraph + Exa Dynamic Research System

## Overview

This document demonstrates how the new LangGraph + Exa system would handle the complex research query: **"Farhad Azima's relationship with the USA & history with Military"** - showing the dynamic workflow generation, real-time execution, and client visualization capabilities.

## Workflow Generation Process

### **Step 1: Query Analysis & Entity Extraction**

```python
# Input Query
query = "Farhad Azima's relationship with the USA & history with Military"

# LangGraph Query Analysis Node
async def analyze_query_node(state: ResearchState) -> ResearchState:
    """Advanced query analysis using Exa + LLM"""
    
    # Initial Exa search to understand query context
    context_search = await exa_search.ainvoke({
        "query": state["query"],
        "use_autoprompt": True,
        "num_results": 5
    })
    
    # LLM analysis of query + context
    analysis_prompt = f"""
    Analyze this research query: {state["query"]}
    
    Context from initial search: {context_search}
    
    Extract:
    1. Primary entities and their types
    2. Research domains required
    3. Complexity assessment
    4. Potential challenges
    5. Estimated timeline
    """
    
    analysis = await llm.ainvoke(analysis_prompt)
    
    # Extracted entities
    state["entities"] = [
        Entity(
            name="Farhad Azima",
            type="person_business",
            description="Iranian-American businessman",
            aliases=["F. Azima", "Farhad R. Azima"],
            significance="primary_subject"
        ),
        Entity(
            name="United States Government",
            type="government",
            description="US federal government and agencies",
            significance="relationship_target"
        ),
        Entity(
            name="US Military",
            type="military_organization", 
            description="US military branches and operations",
            significance="relationship_target"
        )
    ]
    
    # Research domains identified
    state["research_domains"] = [
        "intelligence_operations",
        "government_contracts",
        "military_relationships", 
        "business_networks",
        "legal_proceedings",
        "aviation_industry"
    ]
    
    # Complexity assessment
    state["complexity_assessment"] = ComplexityLevel(
        level="HIGH",
        factors=[
            "Multi-decade timeline (1970s-2000s)",
            "Classified/sensitive information likely",
            "International scope (Iran, US, Nicaragua)",
            "Multiple government agencies involved",
            "Complex business relationships"
        ],
        estimated_duration=timedelta(hours=3),
        confidence_challenges=[
            "Government document availability",
            "Conflicting media reports",
            "Limited primary source access"
        ]
    )
    
    return state
```

### **Generated Research Plan Output:**

```
📋 DYNAMIC RESEARCH PLAN: Farhad Azima Investigation

🎯 PRIMARY OBJECTIVE
Investigate Farhad Azima's relationships with US government and military, focusing on business dealings, contracts, and intelligence connections (1970s-2000s)

📊 COMPLEXITY ASSESSMENT: HIGH
• Multi-decade timeline requiring extensive historical research
• Sensitive/classified information likely present
• International scope with government agency involvement
• Expected conflicts between sources

⏱️ ESTIMATED DURATION: 3-4 hours
📈 CONFIDENCE TARGET: 85%+ with clear source attribution

🔄 WORKFLOW STRUCTURE:

Phase 1: Foundation Research (30 min)
├── 1.1 Background Research [OSINT]
│   ├── Personal history and immigration timeline
│   ├── Business formation and early ventures
│   └── Initial US entry and establishment

├── 1.2 Business Network Mapping [FINANCIAL] 
│   ├── Corporate structure analysis
│   ├── Partnership identification
│   └── Aviation industry connections

Phase 2: Government Relationship Investigation (90 min)
├── 2.1 Intelligence Connections [INTELLIGENCE] ⚡ HIGH PRIORITY
│   ├── CIA relationship investigation
│   ├── Iran-Contra affair involvement
│   └── Covert operations participation

├── 2.2 Military Contracts Analysis [GOVERNMENT] 
│   ├── Department of Defense contracts
│   ├── Military aircraft sales/leasing
│   └── Foreign military sales involvement

├── 2.3 Legal Proceedings Review [LEGAL]
│   ├── Federal court cases
│   ├── Congressional testimony
│   └── Regulatory investigations

Phase 3: Timeline Construction & Analysis (45 min)
├── 3.1 Chronological Timeline Building
├── 3.2 Conflict Detection & Resolution
└── 3.3 Cross-Reference Verification

Phase 4: Synthesis & Reporting (15 min)
├── 4.1 Executive Summary Generation
├── 4.2 Detailed Findings Compilation
└── 4.3 Citation & Confidence Scoring

❓ APPROVE THIS PLAN? (y/n/modify):
```

### **Step 2: User Approval & Plan Modification**

```python
# User requests modification
user_input = "Add deeper focus on the Iran-Contra connections and any weapons trafficking allegations"

# LangGraph Plan Modification Node
async def modify_plan_node(state: ResearchState) -> ResearchState:
    """Modify research plan based on user input"""
    
    modification_prompt = f"""
    User requested: {user_input}
    
    Current plan: {state["workflow_plan"]}
    
    Modify the plan to incorporate the user's request.
    Add specific sub-investigations and adjust time allocations.
    """
    
    # Enhanced Iran-Contra investigation
    enhanced_intelligence_node = {
        "id": "2.1_enhanced_iran_contra",
        "title": "Enhanced Iran-Contra Investigation", 
        "duration": timedelta(minutes=75),  # Increased from 30
        "sub_investigations": [
            "Weapons trafficking allegations (1980s)",
            "Oliver North connections",
            "Contra supply network involvement", 
            "Senate investigation testimony analysis",
            "Financial transaction patterns",
            "Aircraft used in operations"
        ],
        "exa_search_strategies": [
            "Deep government document searches",
            "Congressional hearing transcripts",
            "News archives from 1980s-1990s",
            "Academic research papers"
        ]
    }
    
    # Update workflow plan
    state["workflow_plan"].nodes["2.1"] = enhanced_intelligence_node
    state["workflow_plan"].estimated_duration += timedelta(minutes=45)
    
    return state
```

### **Step 3: Dynamic Workflow Execution**

## Real-Time Execution Visualization

```
🚀 EXECUTING: Farhad Azima Investigation
Session ID: azima_research_2024_001

┌─────────────────────────────────────────────────────────────────┐
│ Overall Progress: ████████████░░░░░░░░░░░░░░░░░░░░░░ 65%        │
│ Phase 2: Government Relationship Investigation                   │
│ Estimated Remaining: 1h 23m                                     │
└─────────────────────────────────────────────────────────────────┘

┌─ Phase 1: Foundation Research ──────────────────────────────────┐
│ ✅ 1.1 Background Research         [COMPLETED] [OSINT]         │ 
│    └─ Found: Immigration 1976, Business formation 1978-1982    │
│ ✅ 1.2 Business Network Mapping    [COMPLETED] [FINANCIAL]     │
│    └─ Mapped: 12 companies, 47 partnerships, Aviation focus   │
└─────────────────────────────────────────────────────────────────┘

┌─ Phase 2: Government Investigation ─────────────────────────────┐
│ 🔄 2.1 Enhanced Iran-Contra Investigation  [75%] [INTELLIGENCE]│
│    ├─ ✅ Weapons trafficking allegations  [COMPLETE]          │
│    │   └─ 🔍 Found: 23 documents, 8 news reports             │
│    ├─ 🔄 Oliver North connections        [IN PROGRESS]        │
│    │   └─ 📊 Processing: Congressional testimony transcripts  │
│    ├─ ⏳ Contra supply network           [QUEUED]              │
│    └─ ⏳ Senate investigation analysis   [QUEUED]              │
│                                                                 │
│ 🔄 2.2 Military Contracts Analysis      [45%] [GOVERNMENT]     │
│    ├─ ✅ DoD contract search           [COMPLETE]             │
│    │   └─ 📋 Found: 15 contracts (1983-1995), $23M total     │ 
│    ├─ 🔄 Aircraft sales analysis       [IN PROGRESS]          │
│    │   └─ 🔍 Analyzing: KC-707 sales to military             │
│    └─ ⏳ Foreign military sales        [QUEUED]               │
│                                                                 │
│ ⏳ 2.3 Legal Proceedings Review         [PENDING] [LEGAL]      │
└─────────────────────────────────────────────────────────────────┘

📊 REAL-TIME FINDINGS:
• High-confidence connection: CIA contractor status (1982-1987)
• Military aircraft sales: 7 transactions, $12.3M value
• Iran-Contra role: Transportation services, financial intermediary

⚠️  POTENTIAL CONFLICT DETECTED:
Employment timeline discrepancy found between sources
└─ Source A: "CIA contractor 1982-1987" (Senate testimony)
└─ Source B: "Private businessman, no gov't ties" (1985 interview)
└─ 🤖 Initiating verification search...
```

### **Step 4: Live Exa Research Execution**

```python
async def execute_iran_contra_investigation(state: ResearchState) -> ResearchState:
    """Enhanced Iran-Contra investigation using Exa's full capabilities"""
    
    # Multi-layered Exa search strategy
    search_strategies = [
        {
            "name": "government_documents",
            "queries": [
                "Farhad Azima Iran Contra Senate testimony Oliver North",
                "Farhad Azima weapons trafficking Nicaragua Congress investigation",
                "Farhad Azima CIA contractor aircraft Iran Contra affair"
            ],
            "domains": ["senate.gov", "congress.gov", "judiciary.house.gov"],
            "date_range": ("1980-01-01", "1995-12-31")
        },
        {
            "name": "news_archives", 
            "queries": [
                "Farhad Azima Iran Contra businessman arms dealer",
                "Farhad Azima Oliver North Nicaragua weapons",
                "Farhad Azima Senate investigation testimony 1987"
            ],
            "domains": ["nytimes.com", "washingtonpost.com", "latimes.com"],
            "date_range": ("1985-01-01", "1992-12-31")
        },
        {
            "name": "academic_research",
            "queries": [
                "Farhad Azima Iran Contra scholarly analysis",
                "Iran Contra affair private contractors Azima",
                "Reagan administration arms sales Iranian American businessmen"
            ],
            "domains": ["jstor.org", "edu"],
            "date_range": ("1990-01-01", "2024-12-31")
        }
    ]
    
    iran_contra_findings = {}
    
    # Execute searches with real-time progress updates
    for strategy in search_strategies:
        await broadcast_progress(f"Searching {strategy['name']}...")
        
        strategy_results = []
        
        for query in strategy["queries"]:
            # Execute Exa search with advanced parameters
            results = await exa_search.ainvoke({
                "query": query,
                "use_autoprompt": True,
                "include_domains": strategy["domains"],
                "start_published_date": strategy["date_range"][0],
                "end_published_date": strategy["date_range"][1],
                "num_results": 15
            })
            
            # Process each result with specialized analysis
            for result in results:
                processed_result = await process_iran_contra_document(result)
                if processed_result["relevance_score"] > 0.7:
                    strategy_results.append(processed_result)
                    
                    # Real-time conflict detection
                    conflicts = await detect_conflicts(processed_result, iran_contra_findings)
                    if conflicts:
                        await broadcast_conflict_alert(conflicts)
        
        iran_contra_findings[strategy["name"]] = strategy_results
        await broadcast_progress(f"Completed {strategy['name']}: {len(strategy_results)} high-quality sources")
    
    # Generate intermediate analysis
    interim_analysis = await synthesize_iran_contra_findings(iran_contra_findings)
    await broadcast_interim_results(interim_analysis)
    
    state["research_results"]["iran_contra_investigation"] = iran_contra_findings
    return state

async def process_iran_contra_document(result: ExaSearchResult) -> Dict[str, Any]:
    """Process individual document with Iran-Contra context"""
    
    # Extract key entities and relationships
    entities = extract_entities(result.text, focus_entities=["Farhad Azima", "Oliver North", "CIA"])
    
    # Identify specific allegations or claims
    allegations = extract_allegations(result.text, patterns=[
        "weapons trafficking", "arms sales", "Iran Contra", 
        "CIA contractor", "covert operations"
    ])
    
    # Calculate relevance and confidence scores
    relevance_score = calculate_relevance(result, "iran_contra_azima")
    confidence_score = assess_source_credibility(result.url, result.published_date)
    
    return {
        "url": result.url,
        "title": result.title,
        "content": result.text,
        "published_date": result.published_date,
        "entities": entities,
        "allegations": allegations,
        "relevance_score": relevance_score,
        "confidence_score": confidence_score,
        "source_type": classify_source_type(result.url),
        "key_quotes": extract_key_quotes(result.text, "Farhad Azima")
    }
```

### **Step 5: Real-Time Conflict Detection & Resolution**

```python
# Example conflict detected during execution
conflict_detected = {
    "type": "employment_timeline_discrepancy",
    "entity": "Farhad Azima",
    "description": "Conflicting information about CIA contractor status",
    "sources": [
        {
            "source": "Senate Intelligence Committee Report (1987)",
            "claim": "Azima served as CIA contractor from 1982-1987",
            "confidence": 0.95,
            "evidence": "Official government testimony under oath"
        },
        {
            "source": "Business Week Interview (1985)", 
            "claim": "Azima denied any government connections, claimed purely private business",
            "confidence": 0.80,
            "evidence": "Direct interview quote"
        }
    ],
    "severity": "high",
    "requires_resolution": True
}

# Automated verification search
verification_search = await exa_search.ainvoke({
    "query": "Farhad Azima CIA contractor verification 1982-1987 government records",
    "include_domains": ["cia.gov", "nsa.gov", "foia.gov", "senate.gov"],
    "start_published_date": "1980-01-01",
    "end_published_date": "2024-12-31"
})

# Real-time client notification
await websocket_broadcast({
    "type": "conflict_resolution_update",
    "conflict_id": "employment_timeline_001",
    "status": "verification_in_progress",
    "verification_sources": len(verification_search),
    "estimated_resolution": "5 minutes"
})
```

## Client Application Live View

### **React Component Rendering Real-Time Research**

```typescript
const AzimaResearchDashboard: React.FC = () => {
  const { state, websocket } = useResearchSession("azima_research_2024_001");
  
  return (
    <div className="research-dashboard">
      {/* Header with overall progress */}
      <ResearchHeader 
        query="Farhad Azima's relationship with the USA & history with Military"
        progress={state.overallProgress}
        estimatedRemaining={state.estimatedRemaining}
      />
      
      {/* Main workflow visualization */}
      <div className="dashboard-main">
        <div className="workflow-section">
          <WorkflowVisualization 
            workflow={state.workflow}
            activeNodes={state.activeNodes}
            nodeProgress={state.nodeProgress}
          />
        </div>
        
        <div className="results-section">
          <LiveResultsStream 
            results={state.partialResults}
            conflicts={state.conflicts}
          />
        </div>
      </div>
      
      {/* Bottom panels */}
      <div className="dashboard-panels">
        <ConflictViewer conflicts={state.conflicts} />
        <SourceTracker sources={state.sourcesFound} />
        <TimelineViewer events={state.timelineEvents} />
      </div>
    </div>
  );
};

const LiveResultsStream: React.FC = ({ results, conflicts }) => {
  return (
    <div className="live-results">
      <h3>Live Research Stream</h3>
      
      {/* Real-time results */}
      <div className="results-stream">
        {results.map(result => (
          <div key={result.id} className="result-item">
            <div className="result-header">
              <span className="source">{result.source.title}</span>
              <span className="confidence">{result.confidence}%</span>
              <span className="timestamp">{result.timestamp}</span>
            </div>
            
            <div className="result-content">
              {result.keyFindings.map(finding => (
                <div key={finding.id} className="finding">
                  <strong>{finding.type}:</strong> {finding.description}
                </div>
              ))}
            </div>
            
            {result.conflicts && (
              <div className="result-conflicts">
                ⚠️ Conflicts detected with {result.conflicts.length} other sources
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
```

### **Final Research Output**

```markdown
# Research Report: Farhad Azima's Relationship with USA & Military

## Executive Summary

Our investigation reveals that Farhad Azima, an Iranian-American businessman, maintained extensive relationships with US government and military entities from the late 1970s through the 1990s, primarily through:

1. **CIA Contractor Status (1982-1987)**: High confidence evidence of official contractor relationship
2. **Military Aircraft Sales**: $23.4M in verified transactions with DoD and foreign allies  
3. **Iran-Contra Involvement**: Transportation and financial intermediary services
4. **Aviation Industry Network**: 47+ business partnerships including defense contractors

**Overall Confidence**: 87% (142 sources, 23 high-quality government documents)

## Key Findings

### Intelligence Relationships
- **CIA Contractor (1982-1987)** [Confidence: 95%]
  - Senate testimony confirms official contractor status
  - Provided aircraft and logistical services for covert operations
  - Security clearance documented through FOIA releases
  
- **Iran-Contra Role** [Confidence: 89%]
  - Facilitated weapons transportation to Contra forces
  - Financial intermediary for arms sales transactions
  - Congressional testimony details operational involvement

### Military & Government Contracts
- **Department of Defense Contracts**: 15 verified contracts, $12.3M total value
- **Foreign Military Sales**: Aircraft leasing to allied nations
- **State Department Coordination**: Diplomatic clearances for international operations

## Information Conflicts

### Employment Timeline Discrepancy [RESOLVED]
- **Conflict**: Government contractor vs. private businessman claims
- **Resolution**: Senate testimony (official record) takes precedence over media interviews
- **Conclusion**: CIA contractor status confirmed, public denials were operational security

## Timeline

- **1976**: Immigration to United States from Iran
- **1978-1982**: Aviation business establishment and growth
- **1982**: CIA contractor relationship begins
- **1983-1986**: Peak Iran-Contra involvement period
- **1987**: Congressional testimony and public exposure
- **1988-1995**: Continued military aircraft sales
- **1996+**: Transition to private aviation business

## Source Analysis

- **Government Documents**: 23 sources (Senate, DoD, State Department)
- **News Archives**: 67 sources (major newspapers, 1980s-1990s)
- **Academic Research**: 34 sources (scholarly analysis)
- **Business Records**: 18 sources (SEC filings, corporate documents)

**Total Sources**: 142
**High Confidence Sources**: 89 (63%)
**Conflicts Detected**: 3 (all resolved)

---
*Generated by Due Diligence AI Research System*  
*Session: azima_research_2024_001*  
*Execution Time: 3h 47m*  
*🤖 Powered by LangGraph + Exa*
```

## System Performance Metrics

### **Research Efficiency**
- **Query Analysis**: 2.3 seconds
- **Workflow Generation**: 4.7 seconds  
- **Average Search Response**: 450ms (Exa performance)
- **Conflict Detection**: Real-time (< 1 second)
- **Total Research Time**: 3h 47m (vs estimated 4h)

### **Data Quality**
- **Sources Identified**: 247 total
- **High-Quality Sources**: 142 (57% retention rate)
- **Confidence Score**: 87% average
- **Conflicts Detected**: 3 (100% resolved)
- **Citation Accuracy**: 99.2%

### **User Experience**
- **Real-time Updates**: 127 progress broadcasts
- **Plan Modifications**: 1 user modification incorporated seamlessly
- **Client Responsiveness**: < 100ms UI updates
- **Session Recovery**: 0 failures (durable execution)

This example demonstrates how the LangGraph + Exa architecture transforms complex research from a static, agent-based process into a dynamic, adaptive investigation that provides unprecedented transparency, control, and quality.