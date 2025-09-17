"""
Test cases for the Research Agent
"""

import pytest
from src.agents.task_agents.research import ResearchAgent
from src.state.definitions import ResearchTask


@pytest.mark.asyncio
async def test_research_agent():
    """Test the Research Agent initialization and tool setup"""

    # Test 1: Agent initialization
    agent = ResearchAgent()
    assert agent is not None
    assert agent.model_name is not None
    assert len(agent.tools) > 0

    # Test 2: Agent creation (LangGraph)
    langgraph_agent = agent.create_agent()
    assert langgraph_agent is not None

    # Test 3: Mock task execution
    task = ResearchTask(
        description="Research Tesla Inc company overview",
        assigned_agent="research",
        output_schema={
            "company_name": "str",
            "industry": "str",
            "description": "str",
            "headquarters": "str",
            "founded": "str"
        }
    )

    # Execute the task
    result = await agent.execute_task(task, context="Due diligence research")
    
    assert result is not None
    assert "task_id" in result
    assert "results" in result
    assert "citations" in result
    assert "confidence" in result