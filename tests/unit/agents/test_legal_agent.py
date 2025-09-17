"""
Test cases for the Legal Agent
"""

import pytest
from src.agents.task_agents.legal import LegalAgent
from src.state.definitions import ResearchTask


@pytest.mark.asyncio
async def test_legal_agent():
    """Test the Legal Agent initialization and tool setup"""

    # Test 1: Agent initialization
    agent = LegalAgent()
    assert agent is not None
    assert agent.model_name is not None
    assert len(agent.tools) > 0

    # Test 2: Agent creation (LangGraph)
    langgraph_agent = agent.create_agent()
    assert langgraph_agent is not None

    # Test 3: Mock task execution
    task = ResearchTask(
        description="Legal analysis of Tesla Inc including litigation, compliance, and sanctions screening",
        assigned_agent="legal",
        output_schema={
            "litigation_status": "str",
            "sanctions_screening": "str",
            "compliance_status": "str",
            "regulatory_issues": "list",
            "legal_risk_assessment": "str"
        }
    )

    # Execute the task
    result = await agent.execute_task(task, context="Due diligence legal analysis")
    
    assert result is not None
    assert "task_id" in result
    assert "results" in result
    assert "citations" in result
    assert "confidence" in result