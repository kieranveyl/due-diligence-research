import asyncio
from typing import Literal

from langgraph.graph import END, START, StateGraph

from src.agents.planner import PlanningAgent
from src.agents.supervisor import SupervisorAgent
from src.agents.task_agents.financial import FinancialAgent
from src.agents.task_agents.legal import LegalAgent
from src.agents.task_agents.osint import OSINTAgent
from src.agents.task_agents.research import ResearchAgent
from src.agents.task_agents.verification import VerificationAgent
from src.state.checkpointer import checkpointer_factory
from src.state.definitions import DueDiligenceState, TaskStatus


class DueDiligenceWorkflow:
    def __init__(self, disable_checkpointing: bool = False):
        self.supervisor = SupervisorAgent()
        self.planner = PlanningAgent()
        self.research_agent = ResearchAgent()
        self.financial_agent = FinancialAgent()
        self.legal_agent = LegalAgent()
        self.osint_agent = OSINTAgent()
        self.verification_agent = VerificationAgent()
        # Initialize other agents as needed

        self.disable_checkpointing = disable_checkpointing
        self.checkpointer = None
        self.graph = self._build_graph()
        self.compiled = None

    async def _ensure_compiled(self):
        """Ensure the graph is compiled with checkpointer"""
        if self.compiled is None:
            if self.disable_checkpointing:
                # For testing - compile without checkpointer
                self.compiled = self.graph.compile()
                self.checkpointer = None
            else:
                try:
                    if self.checkpointer is None:
                        self.checkpointer = await checkpointer_factory.create_checkpointer()
                    if self.checkpointer is not None:
                        self.compiled = self.graph.compile(checkpointer=self.checkpointer)
                    else:
                        self.compiled = self.graph.compile()
                except Exception:
                    # Fallback for testing - compile without checkpointer
                    self.compiled = self.graph.compile()
                    self.checkpointer = None
        return self.compiled

    def _build_graph(self) -> StateGraph:
        """Build the complete multi-agent graph"""

        # Initialize graph
        graph = StateGraph(DueDiligenceState)

        # Add nodes
        graph.add_node("supervisor", self.supervisor.create_agent())
        graph.add_node("planner", self._planner_node)
        graph.add_node("task_executor", self._task_executor_node)
        graph.add_node("research", self.research_agent.create_agent())
        graph.add_node("financial", self.financial_agent.create_agent())
        graph.add_node("legal", self.legal_agent.create_agent())
        graph.add_node("osint", self.osint_agent.create_agent())
        graph.add_node("verification", self.verification_agent.create_agent())
        # Add other agent nodes as implemented

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
                "complete": "supervisor"
            }
        )

        # Task agents return to task executor
        graph.add_edge("research", "task_executor")
        graph.add_edge("financial", "task_executor")
        graph.add_edge("legal", "task_executor")
        graph.add_edge("osint", "task_executor")
        graph.add_edge("verification", "task_executor")

        graph.add_edge("supervisor", END)

        return graph

    async def _planner_node(self, state: DueDiligenceState) -> DueDiligenceState:
        """Planning node implementation"""
        plan_result = await self.planner.plan(state)

        return {
            **state,
            "research_plan": plan_result["research_plan"],
            "tasks": plan_result["tasks"],
            "metadata": {**state.get("metadata", {}), **plan_result["metadata"]}
        }

    async def _task_executor_node(self, state: DueDiligenceState) -> DueDiligenceState:
        """Task execution coordinator"""
        pending_tasks = [t for t in state["tasks"] if t.status == TaskStatus.PENDING]

        if not pending_tasks:
            return {**state, "ready_for_synthesis": True}

        # Execute tasks in parallel batches
        batch_size = min(len(pending_tasks), 3)  # Limit parallel execution

        for i in range(0, len(pending_tasks), batch_size):
            batch = pending_tasks[i:i+batch_size]

            # Mark tasks as in progress
            for task in batch:
                task.status = TaskStatus.IN_PROGRESS

            # Execute batch
            results = await asyncio.gather(*[
                self._execute_single_task(task, state)
                for task in batch
            ])

            # Update task results
            for task, result in zip(batch, results, strict=False):
                if result:
                    task.results = result["results"]
                    task.citations = result["citations"]
                    task.confidence_score = result["confidence"]
                    task.status = TaskStatus.COMPLETED
                else:
                    task.status = TaskStatus.FAILED

        return state

    async def _execute_single_task(self, task, state):
        """Execute a single task based on assigned agent"""
        try:
            if task.assigned_agent == "research":
                return await self.research_agent.execute_task(task)
            elif task.assigned_agent == "financial":
                return await self.financial_agent.execute_task(task)
            elif task.assigned_agent == "legal":
                return await self.legal_agent.execute_task(task)
            elif task.assigned_agent == "osint":
                return await self.osint_agent.execute_task(task)
            elif task.assigned_agent == "verification":
                return await self.verification_agent.execute_task(task)
            # Add other agents as implemented
            return None
        except Exception as e:
            print(f"Task execution failed: {e}")
            return None

    def _route_tasks(self, state: DueDiligenceState) -> Literal["research", "financial", "legal", "osint", "verification", "complete"]:
        """Route to appropriate task agent or completion"""

        # Check for pending tasks
        for task in state["tasks"]:
            if task.status == TaskStatus.PENDING:
                return task.assigned_agent

        return "complete"

    async def run(self, query: str, entity_type: str, entity_name: str, thread_id: str = None):
        """Run workflow with persistence"""

        if not thread_id:
            import uuid
            thread_id = str(uuid.uuid4())

        # Only use config with checkpointer if available
        config = None
        if self.checkpointer is not None:
            config = {
                "configurable": {
                    "thread_id": thread_id,
                    "checkpoint_ns": "due_diligence"
                }
            }

        initial_state = {
            "messages": [],
            "query": query,
            "entity_type": entity_type,
            "entity_name": entity_name,
            "tasks": [],
            "research_plan": "",
            "raw_findings": {},
            "synthesized_report": "",
            "citations": [],
            "confidence_scores": {},
            "thread_id": thread_id,
            "session_id": thread_id,  # For now, same as thread_id
            "user_id": None,
            "metadata": {},
            "ready_for_synthesis": False,
            "human_feedback_required": False,
            "completed": False
        }

        # Ensure graph is compiled with checkpointer
        compiled_graph = await self._ensure_compiled()

        # Stream results with or without checkpointing
        if config:
            async for event in compiled_graph.astream(initial_state, config=config):
                yield event
        else:
            async for event in compiled_graph.astream(initial_state):
                yield event
