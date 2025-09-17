"""
Test cases for the Verification Agent
"""

import pytest
from src.agents.task_agents.verification import VerificationAgent
from src.state.definitions import ResearchTask


@pytest.mark.asyncio
async def test_verification_agent():
    """Test the Verification Agent initialization and tool setup"""

    # Test 1: Agent initialization
    agent = VerificationAgent()
    assert agent is not None
    assert agent.model_name is not None
    assert len(agent.tools) > 0

    # Test 2: Agent creation (LangGraph)
    langgraph_agent = agent.create_agent()
    assert langgraph_agent is not None

    # Test 3: Mock task execution
    task = ResearchTask(
        description="Verify Tesla Inc financial claims including revenue figures, employee count, and founding date",
        assigned_agent="verification",
        output_schema={
            "verification_summary": "str",
            "verified_claims": "list",
            "unverified_claims": "list",
            "source_credibility": "str",
            "confidence_score": "float"
        }
    )

    # Execute the task
    result = await agent.execute_task(task, context="Due diligence fact verification")
    
    assert result is not None
    assert "task_id" in result
    assert "results" in result
    assert "citations" in result
    assert "confidence" in result