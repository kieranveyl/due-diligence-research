"""
Test cases for the Financial Agent
"""

import pytest
from src.agents.task_agents.financial import FinancialAgent
from src.state.definitions import ResearchTask


@pytest.mark.asyncio
async def test_financial_agent():
    """Test the Financial Agent initialization and tool setup"""

    # Test 1: Agent initialization
    agent = FinancialAgent()
    assert agent is not None
    assert agent.model_name is not None
    assert len(agent.tools) > 0

    # Test 2: Agent creation (LangGraph)
    langgraph_agent = agent.create_agent()
    assert langgraph_agent is not None

    # Test 3: Mock task execution
    task = ResearchTask(
        description="Analyze Tesla Inc financial performance and SEC filings",
        assigned_agent="financial",
        output_schema={
            "revenue": "str",
            "profit_margin": "str",
            "debt_ratio": "str",
            "recent_filings": "list",
            "financial_health": "str"
        }
    )

    # Execute the task
    result = await agent.execute_task(task, context="Due diligence financial analysis")
    
    assert result is not None
    assert "task_id" in result
    assert "results" in result
    assert "citations" in result
    assert "confidence" in result
