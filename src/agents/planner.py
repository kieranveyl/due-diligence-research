import json
from typing import Any

from langchain_openai import ChatOpenAI

from src.config.settings import settings
from src.state.definitions import (
    DueDiligenceState,
    EntityType,
    ResearchTask,
    TaskStatus,
)


class PlanningAgent:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.default_model
        self.model = ChatOpenAI(
            model=self.model_name,
            temperature=settings.default_temperature,
            api_key=settings.openai_api_key
        )

    async def plan(self, state: DueDiligenceState) -> dict[str, Any]:
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

    async def _analyze_query(self, query: str) -> dict[str, Any]:
        """Analyze query complexity and requirements"""

        prompt = f"""
        Analyze this due diligence query: "{query}"

        Provide a JSON response with:
        - complexity: "simple", "moderate", or "complex"
        - estimated_time: estimated completion time in minutes
        - key_areas: list of research areas needed
        - risk_level: "low", "medium", or "high"
        """

        response = await self.model.ainvoke(prompt)

        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback default
            return {
                "complexity": "moderate",
                "estimated_time": 15,
                "key_areas": ["background", "compliance"],
                "risk_level": "medium"
            }

    async def _generate_plan(self, query: str, entity_type: EntityType, entity_name: str) -> dict[str, Any]:
        """Generate comprehensive research plan"""

        prompt = f"""
        Create a comprehensive due diligence research plan for:
        Entity: {entity_name}
        Type: {entity_type}
        Query: {query}

        Return a JSON plan with:
        {{
            "strategy": "Overall research strategy description",
            "tasks": [
                {{
                    "description": "Task description",
                    "priority": 1-10,
                    "agent": "research|financial|legal|osint|verification",
                    "output_schema": {{"expected_fields": ["field1", "field2"]}}
                }}
            ],
            "required_agents": ["list", "of", "agents"],
            "dependencies": {{"task_id": ["dependent_task_ids"]}}
        }}

        Focus on creating 3-5 parallel tasks that don't depend on each other.
        """

        response = await self.model.ainvoke(prompt)

        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback plan
            return {
                "strategy": f"Comprehensive due diligence research on {entity_name}",
                "tasks": [
                    {
                        "description": f"Background research on {entity_name}",
                        "priority": 5,
                        "agent": "research",
                        "output_schema": {"background": "str", "key_facts": "list"}
                    }
                ],
                "required_agents": ["research"],
                "dependencies": {}
            }

    def _create_tasks(self, plan: dict, analysis: dict) -> list[ResearchTask]:
        """Create parallel task specifications"""
        tasks = []

        for _idx, task_spec in enumerate(plan.get("tasks", [])):
            task = ResearchTask(
                description=task_spec["description"],
                priority=task_spec.get("priority", 5),
                status=TaskStatus.PENDING,
                assigned_agent=task_spec["agent"],
                output_schema=task_spec.get("output_schema", {})
            )
            tasks.append(task)

        return tasks
