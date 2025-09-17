#!/usr/bin/env python3
"""
Test script for the Legal Agent with LangChain integrations
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.agents.task_agents.legal import LegalAgent
from src.state.definitions import ResearchTask


async def test_legal_agent():
    """Test the Legal Agent initialization and tool setup"""

    print("⚖️ Testing Legal Agent v2.0 with LangChain integrations...")
    print()

    # Set temporary API key for testing if not present
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "sk-test-dummy-key-for-testing"
        print("⚠️ Using dummy OpenAI API key for testing")

        # Reload settings to pick up the new environment variable
        from src.config.settings import Settings
        global settings
        settings = Settings()

    # Test 1: Agent initialization
    try:
        agent = LegalAgent()
        print("✅ Legal Agent initialized successfully")
        print(f"   Model: {agent.model_name}")
        print(f"   Tools available: {len(agent.tools)}")
        for i, tool in enumerate(agent.tools):
            print(f"   {i+1}. {tool.name}: {tool.description}")
    except Exception as e:
        print(f"❌ Failed to initialize Legal Agent: {e}")
        return

    print()

    # Test 2: Settings validation
    print("🔑 API Key Status:")
    print(f"   OpenAI: {'✅' if settings.has_openai_key else '❌'}")
    print(f"   Exa: {'✅' if settings.has_exa_key else '❌'}")
    print(f"   Tavily: {'✅' if settings.has_tavily_key else '❌'}")
    print()

    # Test 3: Agent creation (LangGraph)
    try:
        agent.create_agent()
        print("✅ LangGraph legal agent created successfully")
        print("   Agent name: legal_agent")
    except Exception as e:
        print(f"❌ Failed to create LangGraph legal agent: {e}")
        return

    print()

    # Test 4: Mock task execution
    try:
        # Create a legal analysis task
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

        print("⚖️ Testing legal task execution...")
        print(f"   Task: {task.description}")

        # Execute the task
        result = await agent.execute_task(task, context="Due diligence legal analysis")

        print("✅ Legal task executed successfully")
        print(f"   Task ID: {result['task_id']}")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Citations: {len(result['citations'])} sources")
        print(f"   Results keys: {list(result['results'].keys())}")

    except Exception as e:
        print(f"⚠️ Legal task execution test failed (expected without API keys): {e}")

    print()
    print("🎉 Legal Agent testing completed!")


if __name__ == "__main__":
    asyncio.run(test_legal_agent())
