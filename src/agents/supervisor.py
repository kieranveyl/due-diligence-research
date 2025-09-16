from typing import Annotated

from langchain_core.tools import InjectedToolCallId, tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import InjectedState, create_react_agent
from langgraph.types import Command

from src.config.settings import settings
from src.state.definitions import DueDiligenceState


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
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.default_model
        self.model = ChatOpenAI(
            model=self.model_name,
            temperature=settings.default_temperature,
            api_key=settings.openai_api_key
        )
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
                agent_name="verification",
                description="Delegate to verification agent for fact-checking"
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
            prompt="""You are the supervisor of a multi-agent due diligence system.

            Your responsibilities:
            1. Analyze incoming queries to determine entity type and research scope
            2. Delegate to the planning agent for complex multi-step research
            3. Route specific tasks to specialized agents
            4. Ensure all research is thorough and verified
            5. Coordinate synthesis of findings into comprehensive reports

            Always start with the planning agent for complex queries.
            Ensure verification agent validates critical findings.
            End with synthesis agent for report generation.

            Be concise and direct in your delegations.
            """,
            name="supervisor"
        )
