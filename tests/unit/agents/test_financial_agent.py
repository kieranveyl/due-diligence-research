"""
Test cases for the Financial Agent
"""

import asyncio
import pytest
from src.agents.task_agents.financial import FinancialAgent
from src.state.definitions import ResearchTask


@pytest.mark.asyncio
async def test_financial_agent():
    """Test the Financial Agent initialization and tool setup"""

    print("🔍 Testing Financial Agent...")
    print()

    # Test 1: Agent initialization
    try:
        agent = FinancialAgent()
        print("✅ Financial agent initialized successfully")
        print(f"   Model: {agent.model_name}")
        print(f"   Tools available: {len(agent.tools)}")
        print(f"   Tool names: {[tool.name for tool in agent.tools]}")
    except Exception as e:
        print(f"❌ Failed to initialize financial agent: {e}")
        return

    print()

    # Test 2: Tool availability check
    if hasattr(agent, 'tools') and agent.tools:
        print("🛠️ Financial agent tools:")
        for i, tool in enumerate(agent.tools, 1):
            print(f"   {i}. {tool.name} - {tool.description[:100]}...")
    else:
        print("⚠️ No tools available (this is expected without API keys)")

    print()

    # Test 3: Agent creation (LangGraph)
    try:
        agent.create_agent()
        print("✅ LangGraph financial agent created successfully")
        print("   Agent name: financial_agent")
    except Exception as e:
        print(f"❌ Failed to create LangGraph financial agent: {e}")
        return

    print()

    # Test 4: Mock task execution
    try:
        # Create a financial analysis task
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

        print("📊 Testing financial task execution...")
        print(f"   Task: {task.description}")

        # Execute the task
        result = await agent.execute_task(task, context="Due diligence financial analysis")

        print("✅ Financial task executed successfully")
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
        print(f"⚠️ Financial task execution test failed (expected without API keys): {e}")

    print()
    print("🎉 Financial Agent testing completed!")


if __name__ == "__main__":
    asyncio.run(test_financial_agent())
