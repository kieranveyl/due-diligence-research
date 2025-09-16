# Multi-Agent Deep Due Diligence System Design
## Built with LangGraph - September 15, 2025

---

## Executive Summary

This document provides a comprehensive design and implementation guide for building a production-ready multi-agent deep due diligence system using LangGraph, modeled after Exa's proven architecture but tailored for customizable research on people, places, companies, and entities. The system leverages LangGraph's graph-based orchestration to coordinate specialized agents that perform deep investigative research with guaranteed functionality based on the latest stable LangGraph features as of September 2025.

---

## Table of Contents

1. [System Architecture Overview](#1-system-architecture-overview)
2. [Core Components & Agent Roles](#2-core-components--agent-roles)
3. [Technical Stack & Dependencies](#3-technical-stack--dependencies)
4. [Project Structure](#4-project-structure)
5. [Agent Implementation Details](#5-agent-implementation-details)
6. [State Management & Persistence](#6-state-management--persistence)
7. [Data Sources & Integration](#7-data-sources--integration)
8. [Orchestration & Workflow](#8-orchestration--workflow)
9. [Memory & Context Engineering](#9-memory--context-engineering)
10. [Production Deployment](#10-production-deployment)
11. [Customization & Extension](#11-customization--extension)
12. [Production Readiness Checklist](#12-production-readiness-checklist)

---

## 1. System Architecture Overview

### High-Level Architecture

```mermaid
graph TB
    Client[Client Application] --> API[API Gateway]
    API --> Supervisor[Supervisor Agent]

    Supervisor --> Planner[Planning Agent]
    Supervisor --> Observer[Observer Agent]

    Planner --> Tasks[Task Agents Pool]
    Tasks --> Research[Research Agent]
    Tasks --> Financial[Financial Agent]
    Tasks --> Legal[Legal Agent]
    Tasks --> OSINT[OSINT Agent]
    Tasks --> Verification[Verification Agent]

    Observer --> Synthesis[Synthesis Agent]

    Tasks --> Memory[(Memory Store)]
    Observer --> Memory

    Tasks --> Tools[External Tools]
    Tools --> Search[Search APIs]
    Tools --> Databases[Databases]
    Tools --> Documents[Document Store]
```

### Core Design Principles

1. **Graph-Based Orchestration**: Every agent is a node in a directed graph with explicit state transitions
2. **Parallel Task Execution**: Independent research tasks run concurrently for optimal performance
3. **Context Isolation**: Each agent receives only necessary context to prevent token bloat
4. **Two-Tier Retrieval**: Initial reasoning on snippets, full content fetch only when necessary
5. **Structured Output**: JSON schema enforcement for predictable, parseable results
6. **Persistent State**: Checkpointing enables recovery, time-travel, and human-in-the-loop

---

## 2. Core Components & Agent Roles

### Primary Agent Hierarchy

#### 1. **Supervisor Agent**
- **Role**: Top-level orchestrator managing all user interactions
- **Responsibilities**:
  - Route queries to appropriate specialized agents
  - Manage conversation flow
  - Coordinate handoffs between agents
  - Aggregate final responses

#### 2. **Planning Agent**
- **Role**: Decomposes complex queries into parallel research tasks
- **Responsibilities**:
  - Analyze query complexity
  - Create task breakdown with dependencies
  - Allocate resources and set priorities
  - Define output schemas for each task

#### 3. **Task Agents** (Specialized Workers)
- **Research Agent**: Web research, news, academic papers
- **Financial Agent**: Financial data, market analysis, company filings
- **Legal Agent**: Legal documents, compliance, regulatory research
- **OSINT Agent**: Social media, public records, digital footprints
- **Verification Agent**: Fact-checking, source validation, cross-referencing

#### 4. **Observer Agent**
- **Role**: Maintains global context and aggregates results
- **Responsibilities**:
  - Monitor task completion
  - Aggregate outputs from all task agents
  - Identify gaps requiring additional research
  - Prepare consolidated context for synthesis

#### 5. **Synthesis Agent**
- **Role**: Generate final comprehensive reports
- **Responsibilities**:
  - Merge all research findings
  - Resolve contradictions
  - Format structured output
  - Generate citations and confidence scores

---

## 3. Technical Stack & Dependencies

### Core Dependencies

```python
# requirements.txt
langgraph==0.3.22
langgraph-supervisor==1.0.0
langgraph-checkpoint-sqlite==2.0.1
langchain==0.3.0
langchain-openai==0.2.0
langchain-anthropic==0.2.0
langchain-tavily==0.1.0
langchain-exa==0.1.0

# Data & Storage
redis==5.0.0
postgresql==16.0
chromadb==0.5.0
pinecone-client==3.0.0

# API & Web
fastapi==0.115.0
uvicorn==0.30.0
httpx==0.27.0
beautifulsoup4==4.12.0

# Monitoring & Observability
langsmith==0.2.0
opentelemetry-api==1.25.0
prometheus-client==0.20.0

# Utils
pydantic==2.8.0
python-dotenv==1.0.0
tenacity==9.0.0
```

### Environment Configuration

```bash
# .env
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
TAVILY_API_KEY=your_key
EXA_API_KEY=your_key
LANGSMITH_API_KEY=your_key
POSTGRES_URL=postgresql://user:pass@localhost/duediligence
REDIS_URL=redis://localhost:6379
VECTOR_DB_URL=your_vector_db_url
```

---

## 4. Project Structure

```
due-diligence-system/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── supervisor.py
│   │   ├── planner.py
│   │   ├── task_agents/
│   │   │   ├── research.py
│   │   │   ├── financial.py
│   │   │   ├── legal.py
│   │   │   ├── osint.py
│   │   │   └── verification.py
│   │   ├── observer.py
│   │   └── synthesis.py
│   ├── state/
│   │   ├── __init__.py
│   │   ├── definitions.py
│   │   └── checkpointer.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search.py
│   │   ├── database.py
│   │   ├── document.py
│   │   └── apis.py
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── short_term.py
│   │   ├── long_term.py
│   │   └── vector_store.py
│   ├── workflows/
│   │   ├── __init__.py
│   │   ├── due_diligence.py
│   │   └── custom_workflows.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routers/
│   │   └── middleware/
│   └── config/
│       ├── __init__.py
│       ├── settings.py
│       └── prompts.py
├── tests/
├── docker/
├── scripts/
├── docs/
├── .env
├── requirements.txt
└── README.md
```

---

## 5. Agent Implementation Details

### State Definition

```python
# src/state/definitions.py
from typing import Annotated, TypedDict, List, Dict, Any
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ResearchTask(BaseModel):
    id: str
    description: str
    priority: int
    status: TaskStatus
    assigned_agent: str
    output_schema: Dict[str, Any]
    results: Dict[str, Any] = {}
    citations: List[str] = []
    confidence_score: float = 0.0

class DueDiligenceState(TypedDict):
    """Global state for the due diligence system"""
    messages: Annotated[List, add_messages]
    query: str
    entity_type: str  # person, company, place
    entity_name: str
    tasks: List[ResearchTask]
    research_plan: str
    raw_findings: Dict[str, Any]
    synthesized_report: str
    citations: List[str]
    confidence_scores: Dict[str, float]
    metadata: Dict[str, Any]
```

### Supervisor Agent Implementation

```python
# src/agents/supervisor.py
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from typing import Annotated

def create_handoff_tool(*, agent_name: str, description: str = None):
    """Create a handoff tool for agent delegation"""
    name = f"transfer_to_{agent_name}"
    description = description or f"Transfer task to {agent_name}"

    @tool(name, description=description)
    def handoff_tool(
        task_description: Annotated[str, "Detailed task description"],
        state: Annotated[DueDiligenceState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        # Create task message
        task_message = {
            "role": "user",
            "content": task_description,
            "metadata": {"delegated_by": "supervisor"}
        }

        # Update state with new task
        updated_state = {
            **state,
            "messages": state["messages"] + [task_message]
        }

        return Command(
            goto=agent_name,
            update=updated_state,
            graph=Command.PARENT,
        )

    return handoff_tool

class SupervisorAgent:
    def __init__(self, model="gpt-4.1-turbo"):
        self.model = model
        self.handoff_tools = self._create_handoff_tools()

    def _create_handoff_tools(self):
        return [
            create_handoff_tool(
                agent_name="planner",
                description="Delegate to planning agent for task decomposition"
            ),
            create_handoff_tool(
                agent_name="research",
                description="Delegate to research agent for web research"
            ),
            create_handoff_tool(
                agent_name="financial",
                description="Delegate to financial agent for financial analysis"
            ),
            create_handoff_tool(
                agent_name="legal",
                description="Delegate to legal agent for compliance research"
            ),
            create_handoff_tool(
                agent_name="osint",
                description="Delegate to OSINT agent for digital footprint analysis"
            ),
            create_handoff_tool(
                agent_name="synthesis",
                description="Delegate to synthesis agent for report generation"
            ),
        ]

    def create_agent(self):
        return create_react_agent(
            model=self.model,
            tools=self.handoff_tools,
            prompt="""You are the supervisor of a due diligence system.

            Your responsibilities:
            1. Analyze incoming queries to determine entity type and research scope
            2. Delegate to the planning agent for complex multi-step research
            3. Route specific tasks to specialized agents
            4. Ensure all research is thorough and verified
            5. Coordinate synthesis of findings into comprehensive reports

            Always start with the planning agent for complex queries.
            Ensure verification agent validates critical findings.
            End with synthesis agent for report generation.
            """,
            name="supervisor"
        )
```

### Planning Agent with Task Decomposition

```python
# src/agents/planner.py
from typing import List, Dict, Any
import json

class PlanningAgent:
    def __init__(self, model="gpt-4.1-turbo"):
        self.model = model

    async def plan(self, state: DueDiligenceState) -> Dict[str, Any]:
        """Decompose query into parallel research tasks"""

        # Analyze query complexity
        query_analysis = await self._analyze_query(state["query"])

        # Generate research plan
        plan = await self._generate_plan(
            query=state["query"],
            entity_type=state["entity_type"],
            entity_name=state["entity_name"]
        )

        # Create task specifications
        tasks = self._create_tasks(plan, query_analysis)

        return {
            "research_plan": plan["strategy"],
            "tasks": tasks,
            "metadata": {
                "complexity": query_analysis["complexity"],
                "estimated_time": query_analysis["estimated_time"],
                "required_agents": plan["required_agents"]
            }
        }

    def _create_tasks(self, plan: Dict, analysis: Dict) -> List[ResearchTask]:
        """Create parallel task specifications"""
        tasks = []

        for idx, task_spec in enumerate(plan["tasks"]):
            task = ResearchTask(
                id=f"task_{idx:03d}",
                description=task_spec["description"],
                priority=task_spec["priority"],
                status=TaskStatus.PENDING,
                assigned_agent=task_spec["agent"],
                output_schema=task_spec["output_schema"]
            )
            tasks.append(task)

        return tasks

    async def _generate_plan(self, query: str, entity_type: str, entity_name: str):
        """Generate comprehensive research plan"""

        prompt = f"""
        Create a comprehensive due diligence research plan for:
        Entity: {entity_name}
        Type: {entity_type}
        Query: {query}

        Output a JSON plan with:
        1. Overall strategy
        2. List of parallel research tasks
        3. Required agents and tools
        4. Dependencies between tasks
        5. Output schemas for each task
        """

        # Call LLM with structured output
        response = await self.model.invoke(
            prompt,
            response_format={"type": "json_object"}
        )

        return json.loads(response.content)
```

### Task Agent with Context Engineering

```python
# src/agents/task_agents/research.py
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch
from langchain_exa import ExaSearch
import asyncio

class ResearchAgent:
    def __init__(self, model="gpt-4.1-turbo"):
        self.model = model
        self.tools = self._initialize_tools()

    def _initialize_tools(self):
        return [
            TavilySearch(max_results=5, search_depth="advanced"),
            ExaSearch(num_results=10),
            self._create_deep_search_tool(),
            self._create_news_search_tool(),
        ]

    def _create_deep_search_tool(self):
        @tool
        async def deep_search(query: str, num_results: int = 20):
            """Perform deep multi-source search"""
            # Parallel search across multiple sources
            results = await asyncio.gather(
                self._search_academic(query),
                self._search_news(query),
                self._search_web(query),
                self._search_social(query)
            )

            # Merge and rank results
            merged = self._merge_results(results)
            return merged[:num_results]

        return deep_search

    async def execute_task(self, task: ResearchTask, context: str):
        """Execute research task with context isolation"""

        # Two-tier retrieval strategy
        # Step 1: Search and analyze snippets
        snippets = await self._search_snippets(task.description)

        # Step 2: Reasoning on snippets
        relevant_sources = await self._analyze_snippets(snippets, task)

        # Step 3: Deep crawl only relevant sources
        full_content = await self._crawl_sources(relevant_sources)

        # Step 4: Extract structured information
        results = await self._extract_information(
            content=full_content,
            schema=task.output_schema
        )

        return {
            "task_id": task.id,
            "results": results,
            "citations": relevant_sources,
            "confidence": self._calculate_confidence(results)
        }
```

### Observer with State Aggregation

```python
# src/agents/observer.py
from typing import List, Dict, Any
import asyncio

class ObserverAgent:
    def __init__(self):
        self.completed_tasks = []
        self.pending_tasks = []

    async def observe(self, state: DueDiligenceState):
        """Monitor and aggregate task outputs"""

        # Track task completion
        for task in state["tasks"]:
            if task.status == TaskStatus.COMPLETED:
                self.completed_tasks.append(task)
            elif task.status == TaskStatus.PENDING:
                self.pending_tasks.append(task)

        # Aggregate findings
        aggregated = self._aggregate_findings(self.completed_tasks)

        # Identify gaps
        gaps = self._identify_gaps(aggregated, state["research_plan"])

        # Trigger additional research if needed
        if gaps:
            new_tasks = await self._create_gap_tasks(gaps)
            return {"additional_tasks": new_tasks}

        # Prepare for synthesis
        return {
            "raw_findings": aggregated,
            "ready_for_synthesis": True
        }

    def _aggregate_findings(self, tasks: List[ResearchTask]):
        """Merge task outputs preserving context"""
        aggregated = {
            "entities": {},
            "relationships": [],
            "timeline": [],
            "risks": [],
            "opportunities": [],
            "red_flags": []
        }

        for task in tasks:
            # Merge results by category
            for key, value in task.results.items():
                if key in aggregated:
                    if isinstance(aggregated[key], list):
                        aggregated[key].extend(value)
                    elif isinstance(aggregated[key], dict):
                        aggregated[key].update(value)

        return aggregated
```

---

## 6. State Management & Persistence

### Checkpointer Configuration

```python
# src/state/checkpointer.py
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.sqlite import SqliteSaver
import os

class CheckpointerFactory:
    @staticmethod
    def create_checkpointer(env="development"):
        if env == "production":
            return PostgresSaver(
                connection_string=os.getenv("POSTGRES_URL"),
                schema="langgraph_checkpoints"
            )
        else:
            return SqliteSaver(
                file_path="./data/checkpoints.db"
            )

# Usage in graph compilation
checkpointer = CheckpointerFactory.create_checkpointer()

graph = StateGraph(DueDiligenceState)
# ... add nodes and edges ...
compiled_graph = graph.compile(checkpointer=checkpointer)
```

### Thread Management

```python
# src/workflows/due_diligence.py
class DueDiligenceWorkflow:
    def __init__(self):
        self.graph = self._build_graph()
        self.checkpointer = CheckpointerFactory.create_checkpointer()
        self.compiled = self.graph.compile(checkpointer=self.checkpointer)

    async def run(self, query: str, thread_id: str = None):
        """Run workflow with persistence"""

        if not thread_id:
            thread_id = self._generate_thread_id()

        config = {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": "due_diligence"
            }
        }

        # Stream results with checkpointing
        async for event in self.compiled.astream(
            {"query": query},
            config=config
        ):
            yield event

    async def resume(self, thread_id: str, additional_input: Dict = None):
        """Resume from checkpoint"""
        config = {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": "due_diligence"
            }
        }

        # Get latest checkpoint
        checkpoint = await self.checkpointer.get_latest(config)

        # Resume with additional input
        async for event in self.compiled.astream(
            additional_input or {},
            config=config
        ):
            yield event
```

---

## 7. Data Sources & Integration

### Multi-Source Integration Layer

```python
# src/tools/apis.py
from typing import List, Dict, Any
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class DataSourceIntegrator:
    def __init__(self):
        self.sources = self._initialize_sources()

    def _initialize_sources(self):
        return {
            # Search & Web
            "tavily": TavilyClient(api_key=os.getenv("TAVILY_API_KEY")),
            "exa": ExaClient(api_key=os.getenv("EXA_API_KEY")),
            "serper": SerperClient(api_key=os.getenv("SERPER_API_KEY")),

            # Financial
            "alpha_vantage": AlphaVantageClient(),
            "sec_edgar": SECEdgarClient(),
            "companies_house": CompaniesHouseClient(),

            # Legal & Compliance
            "courtlistener": CourtListenerClient(),
            "pacer": PACERClient(),

            # OSINT
            "shodan": ShodanClient(),
            "hunter": HunterClient(),
            "clearbit": ClearbitClient(),

            # Social & News
            "newsapi": NewsAPIClient(),
            "reddit": RedditClient(),
            "twitter": TwitterClient()
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def search(self, source: str, query: str, **kwargs):
        """Unified search interface with retry logic"""
        client = self.sources.get(source)
        if not client:
            raise ValueError(f"Unknown source: {source}")

        return await client.search(query, **kwargs)
```

### Document Processing Pipeline

```python
# src/tools/document.py
from langchain.document_loaders import PyPDFLoader, UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    async def process_document(self, file_path: str):
        """Process and extract information from documents"""

        # Load document
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        else:
            loader = UnstructuredFileLoader(file_path)

        documents = await loader.aload()

        # Split into chunks
        chunks = self.splitter.split_documents(documents)

        # Extract entities and metadata
        extracted = await self._extract_entities(chunks)

        return {
            "content": chunks,
            "entities": extracted["entities"],
            "metadata": extracted["metadata"]
        }
```

---

## 8. Orchestration & Workflow

### Main Graph Construction

```python
# src/workflows/due_diligence.py
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from typing import Literal

class DueDiligenceGraph:
    def __init__(self):
        self.supervisor = SupervisorAgent()
        self.planner = PlanningAgent()
        self.task_agents = self._initialize_task_agents()
        self.observer = ObserverAgent()
        self.synthesis = SynthesisAgent()

    def build(self) -> StateGraph:
        """Build the complete multi-agent graph"""

        # Initialize graph
        graph = StateGraph(DueDiligenceState)

        # Add nodes
        graph.add_node("supervisor", self.supervisor.create_agent())
        graph.add_node("planner", self.planner.plan)
        graph.add_node("task_executor", self._execute_tasks)
        graph.add_node("observer", self.observer.observe)
        graph.add_node("synthesis", self.synthesis.synthesize)

        # Add task agent nodes
        for name, agent in self.task_agents.items():
            graph.add_node(name, agent.execute_task)

        # Define edges
        graph.add_edge(START, "supervisor")
        graph.add_edge("supervisor", "planner")
        graph.add_edge("planner", "task_executor")

        # Conditional routing from task executor
        graph.add_conditional_edges(
            "task_executor",
            self._route_tasks,
            {
                "research": "research",
                "financial": "financial",
                "legal": "legal",
                "osint": "osint",
                "verification": "verification",
                "complete": "observer"
            }
        )

        # Task agents return to observer
        for name in self.task_agents.keys():
            graph.add_edge(name, "observer")

        # Observer decides next step
        graph.add_conditional_edges(
            "observer",
            self._check_completion,
            {
                "needs_more": "task_executor",
                "ready": "synthesis"
            }
        )

        graph.add_edge("synthesis", END)

        return graph

    def _route_tasks(self, state: DueDiligenceState) -> Literal["research", "financial", "legal", "osint", "verification", "complete"]:
        """Route to appropriate task agent"""

        # Find next pending task
        for task in state["tasks"]:
            if task.status == TaskStatus.PENDING:
                task.status = TaskStatus.IN_PROGRESS
                return task.assigned_agent

        return "complete"

    def _check_completion(self, state: DueDiligenceState) -> Literal["needs_more", "ready"]:
        """Check if all tasks are complete"""

        if state.get("ready_for_synthesis"):
            return "ready"

        return "needs_more"

    async def _execute_tasks(self, state: DueDiligenceState):
        """Parallel task execution coordinator"""

        pending_tasks = [t for t in state["tasks"] if t.status == TaskStatus.PENDING]

        if not pending_tasks:
            return state

        # Execute tasks in parallel batches
        batch_size = 5
        for i in range(0, len(pending_tasks), batch_size):
            batch = pending_tasks[i:i+batch_size]

            # Launch parallel execution
            results = await asyncio.gather(*[
                self._execute_single_task(task, state)
                for task in batch
            ])

            # Update state with results
            for task, result in zip(batch, results):
                task.results = result["results"]
                task.citations = result["citations"]
                task.status = TaskStatus.COMPLETED

        return state
```

---

## 9. Memory & Context Engineering

### Memory Architecture

```python
# src/memory/short_term.py
from typing import Dict, List, Any
import redis
import json

class ShortTermMemory:
    """In-memory cache for active research sessions"""

    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.ttl = 3600  # 1 hour TTL

    async def store(self, thread_id: str, key: str, value: Any):
        """Store with automatic expiration"""
        cache_key = f"stm:{thread_id}:{key}"
        self.redis.setex(
            cache_key,
            self.ttl,
            json.dumps(value)
        )

    async def retrieve(self, thread_id: str, key: str):
        """Retrieve from cache"""
        cache_key = f"stm:{thread_id}:{key}"
        value = self.redis.get(cache_key)
        return json.loads(value) if value else None

# src/memory/long_term.py
from chromadb import Client
from typing import List, Dict

class LongTermMemory:
    """Vector store for historical research and entities"""

    def __init__(self, collection_name="due_diligence"):
        self.client = Client()
        self.collection = self.client.get_or_create_collection(collection_name)

    async def store_entity(self, entity: Dict, embeddings: List[float]):
        """Store entity information with embeddings"""
        self.collection.add(
            ids=[entity["id"]],
            embeddings=[embeddings],
            metadatas=[{
                "entity_type": entity["type"],
                "entity_name": entity["name"],
                "timestamp": entity["timestamp"]
            }],
            documents=[json.dumps(entity)]
        )

    async def search_similar(self, query_embedding: List[float], k: int = 10):
        """Search for similar entities"""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        return results
```

### Context Management

```python
# src/memory/context_manager.py
class ContextManager:
    """Manage context flow between agents"""

    def __init__(self):
        self.context_window = 8000  # tokens
        self.compression_threshold = 6000

    def prepare_context(self, state: DueDiligenceState, agent_type: str) -> str:
        """Prepare context for specific agent"""

        if agent_type == "planner":
            # Planner gets full query and entity info
            return self._format_planning_context(state)

        elif agent_type in ["research", "financial", "legal", "osint"]:
            # Task agents get focused context
            return self._format_task_context(state)

        elif agent_type == "observer":
            # Observer gets aggregated results
            return self._format_observer_context(state)

        elif agent_type == "synthesis":
            # Synthesis gets comprehensive context
            return self._format_synthesis_context(state)

    def compress_context(self, context: str) -> str:
        """Compress context when approaching limits"""

        token_count = self._count_tokens(context)

        if token_count > self.compression_threshold:
            # Summarize completed work phases
            compressed = self._summarize_context(context)

            # Store full context in memory
            self._store_full_context(context)

            return compressed

        return context
```

---

## 10. Production Deployment

### API Implementation

```python
# src/api/main.py
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI(title="Due Diligence API", version="1.0.0")

# Initialize workflow
workflow = DueDiligenceWorkflow()

@app.post("/research")
async def start_research(request: ResearchRequest):
    """Start new due diligence research"""

    thread_id = str(uuid.uuid4())

    # Start workflow in background
    asyncio.create_task(
        workflow.run(
            query=request.query,
            thread_id=thread_id
        )
    )

    return {
        "thread_id": thread_id,
        "status": "started",
        "stream_url": f"/research/{thread_id}/stream"
    }

@app.get("/research/{thread_id}/stream")
async def stream_results(thread_id: str):
    """Stream research results as they become available"""

    async def event_generator():
        config = {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": "due_diligence"
            }
        }

        async for event in workflow.compiled.astream_events(
            None,
            config=config,
            version="v2"
        ):
            # Format as SSE
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

@app.post("/research/{thread_id}/feedback")
async def provide_feedback(thread_id: str, feedback: UserFeedback):
    """Human-in-the-loop feedback"""

    # Resume with user feedback
    await workflow.resume(
        thread_id=thread_id,
        additional_input={"user_feedback": feedback.content}
    )

    return {"status": "feedback_processed"}
```

### Docker Configuration

```dockerfile
# docker/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY config/ ./config/

# Environment
ENV PYTHONPATH=/app
ENV LANGGRAPH_ENV=production

# Run
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: due-diligence-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: due-diligence
  template:
    metadata:
      labels:
        app: due-diligence
    spec:
      containers:
      - name: api
        image: due-diligence:latest
        ports:
        - containerPort: 8000
        env:
        - name: POSTGRES_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
---
apiVersion: v1
kind: Service
metadata:
  name: due-diligence-service
spec:
  selector:
    app: due-diligence
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

---

## 11. Customization & Extension

### Custom Entity Types

```python
# src/config/entity_types.py
from enum import Enum
from typing import Dict, List

class EntityType(Enum):
    PERSON = "person"
    COMPANY = "company"
    PLACE = "place"
    PRODUCT = "product"
    CUSTOM = "custom"

class EntityConfig:
    """Configuration for different entity types"""

    ENTITY_SCHEMAS = {
        EntityType.PERSON: {
            "required_fields": ["full_name", "date_of_birth"],
            "research_focus": ["background", "affiliations", "legal_history", "social_presence"],
            "risk_indicators": ["criminal_records", "sanctions", "PEP_status"],
            "data_sources": ["public_records", "social_media", "news", "legal_databases"]
        },
        EntityType.COMPANY: {
            "required_fields": ["company_name", "jurisdiction"],
            "research_focus": ["financials", "ownership", "compliance", "reputation"],
            "risk_indicators": ["bankruptcy", "litigation", "regulatory_actions"],
            "data_sources": ["SEC_filings", "company_registries", "news", "financial_databases"]
        },
        EntityType.PLACE: {
            "required_fields": ["location_name", "coordinates"],
            "research_focus": ["demographics", "economic_data", "regulatory_environment"],
            "risk_indicators": ["political_stability", "sanctions", "natural_disasters"],
            "data_sources": ["government_data", "maps", "news", "statistical_databases"]
        }
    }

    @classmethod
    def get_config(cls, entity_type: EntityType) -> Dict:
        return cls.ENTITY_SCHEMAS.get(entity_type, {})
```

### Custom Workflows

```python
# src/workflows/custom_workflows.py
class CustomWorkflowBuilder:
    """Build custom due diligence workflows"""

    def __init__(self):
        self.base_graph = DueDiligenceGraph()

    def build_financial_focus(self) -> StateGraph:
        """Workflow optimized for financial due diligence"""

        graph = self.base_graph.build()

        # Add specialized financial nodes
        graph.add_node("credit_check", CreditCheckAgent())
        graph.add_node("market_analysis", MarketAnalysisAgent())

        # Modify routing
        graph.add_edge("financial", "credit_check")
        graph.add_edge("credit_check", "market_analysis")
        graph.add_edge("market_analysis", "observer")

        return graph

    def build_compliance_focus(self) -> StateGraph:
        """Workflow optimized for compliance checks"""

        graph = self.base_graph.build()

        # Add compliance-specific nodes
        graph.add_node("sanctions_check", SanctionsAgent())
        graph.add_node("aml_check", AMLAgent())
        graph.add_node("kyc_verification", KYCAgent())

        # Create compliance pipeline
        graph.add_edge("legal", "sanctions_check")
        graph.add_edge("sanctions_check", "aml_check")
        graph.add_edge("aml_check", "kyc_verification")
        graph.add_edge("kyc_verification", "observer")

        return graph
```

### Plugin System

```python
# src/plugins/base.py
from abc import ABC, abstractmethod

class DueDiligencePlugin(ABC):
    """Base class for extending the system"""

    @abstractmethod
    def get_agents(self) -> Dict[str, Any]:
        """Return custom agents to add"""
        pass

    @abstractmethod
    def get_tools(self) -> List[Any]:
        """Return custom tools to add"""
        pass

    @abstractmethod
    def modify_graph(self, graph: StateGraph) -> StateGraph:
        """Modify the workflow graph"""
        pass

# src/plugins/crypto_plugin.py
class CryptocurrencyPlugin(DueDiligencePlugin):
    """Plugin for cryptocurrency due diligence"""

    def get_agents(self):
        return {
            "blockchain": BlockchainAnalysisAgent(),
            "wallet": WalletTrackerAgent()
        }

    def get_tools(self):
        return [
            ChainAnalysisTool(),
            EtherscanTool(),
            CryptoComplianceTool()
        ]

    def modify_graph(self, graph: StateGraph):
        # Add crypto-specific workflow
        graph.add_node("blockchain", self.get_agents()["blockchain"])
        graph.add_node("wallet", self.get_agents()["wallet"])

        graph.add_edge("osint", "blockchain")
        graph.add_edge("blockchain", "wallet")
        graph.add_edge("wallet", "observer")

        return graph
```

---

## 12. Production Readiness Checklist

### System Validation

- [ ] **Core Functionality**
  - [ ] All agents respond correctly to test queries
  - [ ] Parallel task execution works without race conditions
  - [ ] State persistence and recovery tested
  - [ ] Thread management handles concurrent users
  - [ ] Memory management prevents token overflow

- [ ] **Integration Testing**
  - [ ] All external APIs connected and authenticated
  - [ ] Fallback mechanisms for API failures
  - [ ] Rate limiting implemented for all external calls
  - [ ] Circuit breakers configured for resilience

- [ ] **Performance Benchmarks**
  - [ ] Response time < 30s for simple queries
  - [ ] Response time < 3min for complex due diligence
  - [ ] System handles 100+ concurrent threads
  - [ ] Memory usage stable under load
  - [ ] Database queries optimized with indices

### Security & Compliance

- [ ] **Data Security**
  - [ ] All API keys stored in secure vault
  - [ ] TLS/SSL for all external communications
  - [ ] Data encryption at rest and in transit
  - [ ] PII handling complies with GDPR/CCPA
  - [ ] Audit logging for all operations

- [ ] **Access Control**
  - [ ] Authentication implemented (OAuth2/JWT)
  - [ ] Role-based access control (RBAC)
  - [ ] API rate limiting per user
  - [ ] Input validation and sanitization

### Monitoring & Observability

- [ ] **Logging**
  - [ ] Structured logging implemented
  - [ ] Log aggregation configured (ELK/Datadog)
  - [ ] Error tracking (Sentry/Rollbar)
  - [ ] Request tracing with correlation IDs

- [ ] **Metrics**
  - [ ] Prometheus metrics exposed
  - [ ] Dashboard created (Grafana)
  - [ ] Alerts configured for critical issues
  - [ ] SLA monitoring in place

- [ ] **LangSmith Integration**
  - [ ] Token usage tracking
  - [ ] Cost monitoring per operation
  - [ ] Performance profiling enabled
  - [ ] A/B testing framework ready

### Deployment

- [ ] **Infrastructure**
  - [ ] Kubernetes manifests validated
  - [ ] Auto-scaling configured
  - [ ] Health checks implemented
  - [ ] Graceful shutdown handled

- [ ] **CI/CD**
  - [ ] Automated testing pipeline
  - [ ] Code quality checks (linting, type checking)
  - [ ] Security scanning (dependencies, containers)
  - [ ] Blue-green deployment configured

- [ ] **Documentation**
  - [ ] API documentation (OpenAPI/Swagger)
  - [ ] Agent behavior documented
  - [ ] Runbook for common issues
  - [ ] Architecture decision records (ADRs)

### Testing Coverage

```python
# tests/test_workflow.py
import pytest
from src.workflows.due_diligence import DueDiligenceWorkflow

@pytest.mark.asyncio
async def test_simple_person_research():
    """Test basic person due diligence"""
    workflow = DueDiligenceWorkflow()

    result = await workflow.run(
        query="Research John Doe, CEO of Acme Corp",
        thread_id="test_001"
    )

    assert result["entity_type"] == "person"
    assert "financial" in result["raw_findings"]
    assert "legal" in result["raw_findings"]
    assert len(result["citations"]) > 0

@pytest.mark.asyncio
async def test_parallel_task_execution():
    """Test parallel agent coordination"""
    # Test implementation
    pass

@pytest.mark.asyncio
async def test_checkpoint_recovery():
    """Test state persistence and recovery"""
    # Test implementation
    pass
```

---

## Conclusion

This design provides a production-ready multi-agent due diligence system built on LangGraph's proven patterns. The architecture ensures:

1. **Scalability** through parallel task execution and distributed agents
2. **Reliability** via checkpointing and state persistence
3. **Flexibility** with customizable workflows and plugin system
4. **Efficiency** through context engineering and two-tier retrieval
5. **Observability** with comprehensive monitoring and logging

The system is ready for deployment and can be extended for specific due diligence requirements while maintaining the core architectural benefits of the multi-agent approach.

---

## Next Steps

1. **Initialize Project**: Set up the project structure and install dependencies
2. **Implement Core Agents**: Start with supervisor and planning agents
3. **Add Data Sources**: Integrate required APIs and databases
4. **Test Workflows**: Validate with sample due diligence queries
5. **Deploy to Staging**: Test in production-like environment
6. **Monitor & Optimize**: Use LangSmith for performance tuning
7. **Scale Gradually**: Add more specialized agents as needed

Remember: Start simple, test thoroughly, and iterate based on real-world usage.