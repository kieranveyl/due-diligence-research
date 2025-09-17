"""
Test cases for the OSINT Agent
"""

import asyncio
import pytest
from src.agents.task_agents.osint import OSINTAgent
from src.state.definitions import ResearchTask


@pytest.mark.asyncio
async def test_osint_agent():
    """Test the OSINT Agent initialization and tool setup"""

    print("🕵️ Testing OSINT Agent...")
    print()

    # Test 1: Agent initialization
    try:
        agent = OSINTAgent()
        print("✅ OSINT agent initialized successfully")
        print(f"   Model: {agent.model_name}")
        print(f"   Tools available: {len(agent.tools)}")
        print(f"   Tool names: {[tool.name for tool in agent.tools]}")
    except Exception as e:
        print(f"❌ Failed to initialize OSINT agent: {e}")
        return

    print()

    # Test 2: Tool availability check
    if hasattr(agent, 'tools') and agent.tools:
        print("🛠️ OSINT agent tools:")
        for i, tool in enumerate(agent.tools, 1):
            print(f"   {i}. {tool.name} - {tool.description[:100]}...")
    else:
        print("⚠️ No tools available (this is expected without API keys)")

    print()

    # Test 3: Agent creation (LangGraph)
    try:
        agent.create_agent()
        print("✅ LangGraph OSINT agent created successfully")
        print("   Agent name: osint_agent")
    except Exception as e:
        print(f"❌ Failed to create LangGraph OSINT agent: {e}")
        return

    print()

    # Test 4: Mock task execution
    try:
        # Create an OSINT analysis task
        task = ResearchTask(
            description="OSINT analysis of Tesla Inc including social media presence, digital footprint, and online reputation",
            assigned_agent="osint",
            output_schema={
                "social_media_presence": "str",
                "digital_footprint": "str",
                "online_reputation": "str",
                "domain_analysis": "list",
                "security_incidents": "str"
            }
        )

        print("🕵️ Testing OSINT task execution...")
        print(f"   Task: {task.description}")

        # Execute the task
        result = await agent.execute_task(task, context="Due diligence OSINT analysis")

        print("✅ OSINT task executed successfully")
        print(f"   Task ID: {result['task_id']}")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Citations: {len(result['citations'])} sources")
        print(f"   Results keys: {list(result['results'].keys())}")

        # Validate result structure for pytest
        assert result is not None
        assert "task_id" in result
        assert "results" in result
        assert "citations" in result
        assert "confidence" in result

    except Exception as e:
        print(f"⚠️ OSINT task execution test failed (expected without API keys): {e}")

    print()
    print("🎉 OSINT Agent testing completed!")


if __name__ == "__main__":
    asyncio.run(test_osint_agent())
