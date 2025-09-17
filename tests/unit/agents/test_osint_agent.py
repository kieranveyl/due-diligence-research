"""
Test cases for the OSINT Agent
"""

import pytest
from src.agents.task_agents.osint import OSINTAgent
from src.state.definitions import ResearchTask


@pytest.mark.asyncio
async def test_osint_agent():
    """Test the OSINT Agent initialization and tool setup"""

    # Test 1: Agent initialization
    agent = OSINTAgent()
    assert agent is not None
    assert agent.model_name is not None
    assert len(agent.tools) > 0

    # Test 2: Agent creation (LangGraph)
    langgraph_agent = agent.create_agent()
    assert langgraph_agent is not None

    # Test 3: Mock task execution
    task = ResearchTask(
        description="OSINT investigation of Tesla Inc including social media presence, digital footprint, and reputation analysis",
        assigned_agent="osint",
        output_schema={
            "digital_presence": "str",
            "social_media_profiles": "list",
            "reputation_assessment": "str",
            "security_findings": "list",
            "threat_indicators": "str"
        }
    )

    # Execute the task
    result = await agent.execute_task(task, context="Due diligence OSINT investigation")
    
    assert result is not None
    assert "task_id" in result
    assert "results" in result
    assert "citations" in result
    assert "confidence" in result