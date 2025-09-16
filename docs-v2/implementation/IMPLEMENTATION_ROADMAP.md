# Implementation Roadmap: LangGraph + Exa Migration
## From Current System to AI-Native Research Platform

## Overview

This roadmap outlines the complete migration from the current agent-based Due Diligence system to a unified LangGraph + Exa ecosystem. The migration follows a four-phase approach designed to minimize disruption while delivering immediate value at each milestone.

## Current State Analysis

### **Existing System (As Found)**
```
Current Architecture:
├── src/agents/
│   ├── planner.py (PlanningAgent)
│   ├── supervisor.py (SupervisorAgent) 
│   └── task_agents/
│       ├── financial.py (FinancialAgent)
│       ├── legal.py (LegalAgent)
│       ├── osint.py (OSINTAgent)
│       └── verification.py (VerificationAgent)
├── src/workflows/
│   └── due_diligence.py (DueDiligenceWorkflow)
├── src/cli/
│   └── main.py (CLI interface)
└── tests/
    ├── unit/test_agents.py
    └── integration/test_workflow.py

Current Dependencies:
✅ langgraph==0.6.7
✅ langchain-exa==0.3.1  
✅ fastapi==0.115.0
✅ typer==0.9.0 + rich>=13.0.0
✅ PostgreSQL support ready
```

### **Migration Advantages**
- **LangGraph already integrated** - Core framework in place
- **Exa integration available** - langchain-exa package ready
- **Modern Python stack** - Python 3.11+, async/await throughout
- **CLI foundation solid** - Typer + Rich for interactive interfaces
- **Database ready** - PostgreSQL for checkpointing

## Migration Strategy: Parallel Development

Instead of disrupting the current system, we'll build the new architecture alongside it, then switch over when ready.

```
Migration Approach:
├── Phase 1: New Foundation (Keep existing system running)
├── Phase 2: Core Features (Parallel development)  
├── Phase 3: Client App (Add visualization layer)
└── Phase 4: Complete Migration (Switch over + enhance)
```

## Phase 1: Foundation Setup (Weeks 1-2)

### **Week 1: LangGraph + Exa Core Integration**

#### **Day 1-2: New Module Structure**
```bash
# Create new module structure alongside existing
mkdir -p src/langgraph_system/
mkdir -p src/langgraph_system/graphs/
mkdir -p src/langgraph_system/nodes/
mkdir -p src/langgraph_system/exa_integration/
mkdir -p src/langgraph_system/state/
mkdir -p src/client_app/
```

#### **Day 3-4: Core LangGraph Implementation**
```python
# src/langgraph_system/graphs/master_research_graph.py
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSqliteSaver
from langchain_exa import ExaSearchResults

class MasterResearchGraph:
    """New LangGraph-based research orchestrator"""
    
    def __init__(self):
        # Use existing database connection
        self.checkpointer = PostgresSqliteSaver.from_conn_string(
            settings.database_url
        )
        
        # Initialize Exa integration
        self.exa_search = ExaSearchResults(
            exa_api_key=settings.exa_api_key,
            num_results=10
        )
        
        # Build graph
        self.graph = self._build_graph()
        self.compiled = self.graph.compile(checkpointer=self.checkpointer)
    
    def _build_graph(self) -> StateGraph:
        graph = StateGraph(ResearchState)
        
        # Core nodes
        graph.add_node("analyze_query", self.analyze_query_node)
        graph.add_node("generate_workflow", self.generate_workflow_node)
        graph.add_node("execute_research", self.execute_research_node)
        graph.add_node("synthesize_results", self.synthesize_results_node)
        
        # Flow
        graph.add_edge(START, "analyze_query")
        graph.add_edge("analyze_query", "generate_workflow")
        graph.add_edge("generate_workflow", "execute_research")
        graph.add_edge("execute_research", "synthesize_results")
        graph.add_edge("synthesize_results", END)
        
        return graph
```

#### **Day 5-7: Exa Integration Layer**
```python
# src/langgraph_system/exa_integration/exa_research_engine.py
from langchain_exa import ExaSearchResults, ExaFindSimilarResults, ExaCrawlResults

class ExaResearchEngine:
    """Unified Exa research interface"""
    
    def __init__(self):
        self.neural_search = ExaSearchResults(num_results=20)
        self.company_research = ExaFindSimilarResults(num_results=15)
        self.web_crawler = ExaCrawlResults()
    
    async def comprehensive_research(
        self, 
        entity: str, 
        domains: List[str]
    ) -> Dict[str, Any]:
        """Multi-modal Exa research strategy"""
        
        results = {}
        
        # Neural search for broad coverage
        for domain in domains:
            domain_queries = self._generate_domain_queries(entity, domain)
            domain_results = []
            
            for query in domain_queries:
                search_results = await self.neural_search.ainvoke({
                    "query": query,
                    "use_autoprompt": True,
                    "include_domains": self._get_domain_sources(domain),
                    "start_published_date": "1970-01-01"
                })
                
                processed = [
                    self._process_result(r, domain) 
                    for r in search_results
                ]
                domain_results.extend(processed)
            
            results[domain] = domain_results
        
        return results
```

### **Week 2: Basic CLI Integration**
```python
# src/cli/langgraph_commands.py (New command group)
import typer
from rich.console import Console
from rich.progress import Progress

app = typer.Typer()
console = Console()

@app.command()
def research_v2(
    query: str = typer.Argument(..., help="Research query"),
    preview: bool = typer.Option(False, "--preview", help="Preview mode only")
):
    """New LangGraph-powered research command"""
    
    console.print(f"🚀 LangGraph Research: {query}", style="bold blue")
    
    # Initialize new system
    master_graph = MasterResearchGraph()
    
    if preview:
        # Just show what the workflow would be
        with console.status("Analyzing query..."):
            workflow_plan = master_graph.preview_workflow(query)
        
        console.print(workflow_plan)
    else:
        # Execute full research
        with Progress() as progress:
            session_id = f"lg_{uuid.uuid4().hex[:8]}"
            
            async def run_research():
                async for event in master_graph.compiled.astream({
                    "query": query,
                    "session_id": session_id
                }):
                    # Update progress display
                    console.print(f"Node: {event}")
            
            asyncio.run(run_research())

# Add to main CLI
# src/cli/main.py
app.add_typer(langgraph_commands.app, name="v2")
```

## Phase 2: Core Feature Development (Weeks 3-6)

### **Week 3: Dynamic Workflow Generation**
```python
# src/langgraph_system/nodes/query_analysis.py
async def analyze_query_node(state: ResearchState) -> ResearchState:
    """Advanced query analysis with Exa context"""
    
    # Quick Exa search for context
    context_results = await exa_search.ainvoke({
        "query": state["query"],
        "use_autoprompt": True,
        "num_results": 5
    })
    
    # LLM analysis with context
    analysis_prompt = f"""
    Query: {state["query"]}
    Context: {context_results}
    
    Extract:
    1. Primary entities and relationships
    2. Required research domains  
    3. Complexity assessment
    4. Custom workflow requirements
    """
    
    analysis = await llm.ainvoke(analysis_prompt)
    
    # Parse structured output
    state["entities"] = extract_entities(analysis)
    state["research_domains"] = extract_domains(analysis)
    state["complexity"] = assess_complexity(analysis)
    
    return state

# src/langgraph_system/nodes/workflow_generation.py  
async def generate_workflow_node(state: ResearchState) -> ResearchState:
    """Generate custom workflow based on analysis"""
    
    # Create domain-specific subgraphs
    subgraphs = {}
    
    for domain in state["research_domains"]:
        if domain == "intelligence":
            subgraphs[domain] = create_intelligence_subgraph(state["entities"])
        elif domain == "financial":
            subgraphs[domain] = create_financial_subgraph(state["entities"])
        elif domain == "legal":
            subgraphs[domain] = create_legal_subgraph(state["entities"])
        # etc.
    
    # Generate execution plan
    execution_plan = create_execution_plan(subgraphs, state["complexity"])
    
    state["workflow_plan"] = execution_plan
    return state
```

### **Week 4: Real-Time Execution Engine**
```python
# src/langgraph_system/execution/real_time_executor.py
class RealTimeExecutor:
    """Manages real-time workflow execution with progress tracking"""
    
    def __init__(self, websocket_manager):
        self.ws_manager = websocket_manager
        
    async def execute_workflow(
        self, 
        workflow_plan: WorkflowPlan,
        session_id: str
    ) -> Dict[str, Any]:
        """Execute workflow with real-time progress updates"""
        
        results = {}
        
        for level in workflow_plan.execution_levels:
            # Execute nodes in parallel within each level
            level_tasks = []
            
            for node in level.nodes:
                task = self._create_monitored_task(node, session_id)
                level_tasks.append(task)
            
            # Wait for level completion with progress tracking
            level_results = await asyncio.gather(*level_tasks)
            
            # Update results and broadcast
            for i, result in enumerate(level_results):
                node_id = level.nodes[i].id
                results[node_id] = result
                
                await self.ws_manager.broadcast_update(session_id, {
                    "type": "node_completed",
                    "node_id": node_id,
                    "result": result
                })
        
        return results
    
    async def _create_monitored_task(self, node: WorkflowNode, session_id: str):
        """Create task with progress monitoring"""
        
        async def monitored_execution():
            await self.ws_manager.broadcast_update(session_id, {
                "type": "node_started", 
                "node_id": node.id
            })
            
            # Execute with progress callbacks
            result = await node.execute(
                progress_callback=lambda p: self._update_progress(session_id, node.id, p)
            )
            
            return result
        
        return asyncio.create_task(monitored_execution())
```

### **Week 5: Conflict Detection System**
```python
# src/langgraph_system/conflict_detection/real_time_detector.py
class RealTimeConflictDetector:
    """Detects conflicts as research results come in"""
    
    async def process_new_finding(
        self, 
        finding: Finding,
        session_results: Dict[str, Any],
        session_id: str
    ) -> List[Conflict]:
        """Process new finding and detect conflicts"""
        
        conflicts = []
        
        # Compare with existing findings
        for existing_finding in self._get_existing_findings(session_results):
            
            # Temporal conflict check
            if self._check_temporal_conflict(finding, existing_finding):
                conflict = await self._create_temporal_conflict(
                    finding, existing_finding
                )
                conflicts.append(conflict)
            
            # Factual contradiction check
            if await self._check_factual_conflict(finding, existing_finding):
                conflict = await self._create_factual_conflict(
                    finding, existing_finding
                )
                conflicts.append(conflict)
        
        # Broadcast conflicts immediately
        for conflict in conflicts:
            await self._broadcast_conflict(session_id, conflict)
        
        return conflicts
    
    async def _check_factual_conflict(
        self, 
        finding1: Finding, 
        finding2: Finding
    ) -> bool:
        """Use Exa to verify factual contradictions"""
        
        verification_query = f"""
        verify conflicting claims:
        Claim 1: {finding1.content}
        Claim 2: {finding2.content}
        Entity: {finding1.entity}
        """
        
        verification = await exa_search.ainvoke({
            "query": verification_query,
            "use_autoprompt": True,
            "num_results": 5
        })
        
        # Analyze verification results
        conflict_score = await self._analyze_conflict_evidence(verification)
        return conflict_score > 0.7
```

### **Week 6: CLI Enhancement & Testing**
```python
# Enhanced CLI with real-time display
@app.command()
def research(
    query: str,
    interactive: bool = typer.Option(True, "--interactive/--batch"),
    output_format: str = typer.Option("markdown", "--format")
):
    """Enhanced research with real-time progress"""
    
    if interactive:
        # Rich interactive mode
        with Live(generate_progress_layout(), refresh_per_second=10) as live:
            
            async def update_display():
                master_graph = MasterResearchGraph()
                
                async for event in master_graph.compiled.astream({
                    "query": query,
                    "session_id": generate_session_id()
                }):
                    # Update live display
                    layout = update_progress_layout(event)
                    live.update(layout)
            
            asyncio.run(update_display())
    else:
        # Batch mode
        console.print("Running in batch mode...")
        # Run without interactive display
```

## Phase 3: Client Application Development (Weeks 7-10)

### **Week 7: React App Foundation**
```bash
# Create client app
cd src/client_app/
npx create-next-app@latest . --typescript --tailwind --app
npm install @tanstack/react-query ws @types/ws
npm install react-flow-renderer recharts lucide-react
```

### **Week 8: Real-Time WebSocket Integration**
```typescript
// src/client_app/hooks/useResearchSession.ts
export const useResearchSession = (sessionId: string) => {
  const [state, setState] = useState<ResearchSessionState>();
  const [websocket, setWebSocket] = useState<WebSocket>();
  
  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/session/${sessionId}`);
    
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      handleRealTimeUpdate(update, setState);
    };
    
    setWebSocket(ws);
    return () => ws.close();
  }, [sessionId]);
  
  return { state, websocket };
};

// src/client_app/components/WorkflowVisualization.tsx
export const WorkflowVisualization: React.FC = ({ workflow }) => {
  return (
    <ReactFlowProvider>
      <ReactFlow
        nodes={workflow.nodes.map(createNodeComponent)}
        edges={workflow.edges}
        nodeTypes={{ researchNode: ResearchNodeComponent }}
      />
    </ReactFlowProvider>
  );
};
```

### **Week 9: Advanced UI Components**
```typescript
// Real-time conflict viewer
export const ConflictViewer: React.FC = ({ conflicts }) => {
  return (
    <div className="conflict-viewer">
      {conflicts.map(conflict => (
        <ConflictCard key={conflict.id} conflict={conflict} />
      ))}
    </div>
  );
};

// Live results stream
export const LiveResultsStream: React.FC = ({ results }) => {
  return (
    <div className="results-stream">
      {results.map(result => (
        <ResultCard key={result.id} result={result} />
      ))}
    </div>
  );
};
```

### **Week 10: Integration & Polish**
- Connect React app to FastAPI backend
- Implement authentication and session management
- Add export functionality (PDF, etc.)
- Performance optimization

## Phase 4: Complete Migration & Enhancement (Weeks 11-14)

### **Week 11: Migration Testing**
```python
# Migration testing strategy
class MigrationTester:
    """Test equivalence between old and new systems"""
    
    def __init__(self):
        self.old_system = DueDiligenceWorkflow()  # Existing
        self.new_system = MasterResearchGraph()   # New LangGraph
    
    async def test_equivalent_results(self, test_queries: List[str]):
        """Test that new system produces equivalent or better results"""
        
        for query in test_queries:
            # Run both systems
            old_result = await self.old_system.run(query)
            new_result = await self.new_system.compiled.ainvoke({"query": query})
            
            # Compare results
            comparison = await self.compare_results(old_result, new_result)
            
            assert comparison.quality_score >= 0.9, f"Quality degradation for: {query}"
            assert comparison.coverage_score >= 1.0, f"Coverage loss for: {query}"
```

### **Week 12: Performance Optimization**
- Database query optimization
- Exa API usage optimization  
- Concurrent execution tuning
- Memory usage optimization

### **Week 13: Production Deployment**
```yaml
# docker-compose.production.yml
version: '3.8'

services:
  langgraph-system:
    build: .
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/dd_system
      - EXA_API_KEY=${EXA_API_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
  
  client-app:
    build: ./src/client_app
    ports:
      - "3000:3000"
    depends_on:
      - langgraph-system
  
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=dd_system
      - POSTGRES_USER=dd_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
```

### **Week 14: System Cutover**
1. **Final testing** with production data
2. **User training** on new interface
3. **Gradual migration** of active sessions
4. **Old system deprecation** 
5. **Documentation update**

## Success Metrics

### **Performance Targets**
- **Query Analysis**: < 3 seconds
- **Workflow Generation**: < 5 seconds
- **Research Execution**: 25% faster than current system
- **Real-time Updates**: < 500ms latency
- **System Availability**: 99.9%

### **Quality Targets**
- **Source Quality**: 90%+ retention rate (vs current 70%)
- **Conflict Detection**: 95%+ accuracy
- **User Satisfaction**: 90%+ approval rating
- **Research Completeness**: 95%+ comprehensive coverage

### **Business Targets**
- **Research Speed**: 40% faster completion times
- **Cost Efficiency**: 30% reduction in API costs (Exa efficiency)
- **User Adoption**: 80% migration within 3 months
- **Feature Usage**: 60%+ use of new visualization features

## Risk Mitigation

### **Technical Risks**
- **LangGraph Learning Curve**: Mitigated by parallel development approach
- **Exa API Limits**: Mitigated by intelligent caching and rate limiting
- **Database Performance**: Mitigated by PostgreSQL optimization and monitoring
- **Real-time Complexity**: Mitigated by gradual feature rollout

### **Business Risks**
- **User Resistance**: Mitigated by maintaining familiar CLI interface
- **Training Requirements**: Mitigated by intuitive UI design and documentation
- **Migration Downtime**: Mitigated by parallel system approach
- **Feature Parity**: Mitigated by comprehensive testing and gradual migration

This roadmap ensures a smooth transition to the new LangGraph + Exa architecture while delivering immediate value and maintaining system reliability throughout the migration process.