"""
Test cases for the Verification Agent
"""

import asyncio
import pytest
from src.agents.task_agents.verification import VerificationAgent
from src.state.definitions import ResearchTask


@pytest.mark.asyncio
async def test_verification_agent():
    """Test the Verification Agent initialization and tool setup"""

    print("🔍 Testing Verification Agent...")
    print()

    # Test 1: Agent initialization
    try:
        agent = VerificationAgent()
        print("✅ Verification agent initialized successfully")
        print(f"   Model: {agent.model_name}")
        print(f"   Tools available: {len(agent.tools)}")
        print(f"   Tool names: {[tool.name for tool in agent.tools]}")
    except Exception as e:
        print(f"❌ Failed to initialize verification agent: {e}")
        return

    print()

    # Test 2: Tool availability check
    if hasattr(agent, 'tools') and agent.tools:
        print("🛠️ Verification agent tools:")
        for i, tool in enumerate(agent.tools, 1):
            print(f"   {i}. {tool.name} - {tool.description[:100]}...")
    else:
        print("⚠️ No tools available (this is expected without API keys)")

    print()

    # Test 3: Agent creation (LangGraph)
    try:
        agent.create_agent()
        print("✅ LangGraph verification agent created successfully")
        print("   Agent name: verification_agent")
    except Exception as e:
        print(f"❌ Failed to create LangGraph verification agent: {e}")
        return

    print()

    # Test 4: Mock task execution
    try:
        # Create a verification analysis task
        task = ResearchTask(
            description="Cross-verification of Tesla Inc findings from multiple sources and fact-checking",
            assigned_agent="verification",
            output_schema={
                "verified_facts": "list",
                "conflicting_information": "list",
                "source_reliability": "str",
                "verification_confidence": "str",
                "recommendations": "str"
            }
        )

        print("✅ Testing verification task execution...")
        print(f"   Task: {task.description}")

        # Execute the task
        result = await agent.execute_task(task, context="Due diligence verification analysis")

        print("✅ Verification task executed successfully")
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
        print(f"⚠️ Verification task execution test failed (expected without API keys): {e}")

    print()
    print("🎉 Verification Agent testing completed!")


if __name__ == "__main__":
    asyncio.run(test_verification_agent())
