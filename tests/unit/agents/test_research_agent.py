#!/usr/bin/env python3
"""
Test script for the updated Research Agent with LangChain integrations
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.agents.task_agents.research import ResearchAgent
from src.state.definitions import ResearchTask


async def test_research_agent():
    """Test the Research Agent initialization and tool setup"""

    print("🧪 Testing Research Agent v2.0 with LangChain integrations...")
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
        agent = ResearchAgent()
        print("✅ Research Agent initialized successfully")
        print(f"   Model: {agent.model_name}")
        print(f"   Tools available: {len(agent.tools)}")
        for i, tool in enumerate(agent.tools):
            print(f"   {i+1}. {tool.name}: {tool.description}")
    except Exception as e:
        print(f"❌ Failed to initialize Research Agent: {e}")
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
        langgraph_agent = agent.create_agent()
        print("✅ LangGraph agent created successfully")
        print(f"   Agent name: {langgraph_agent.name if hasattr(langgraph_agent, 'name') else 'N/A'}")
    except Exception as e:
        print(f"❌ Failed to create LangGraph agent: {e}")
        return

    print()

    # Test 4: Mock task execution (if we have OpenAI key)
    if settings.has_openai_key:
        try:
            # Create a simple research task
            task = ResearchTask(
                description="Research Tesla Inc company overview",
                assigned_agent="research",
                output_schema={"company_name": "str", "industry": "str", "description": "str"}
            )

            print("🔍 Testing task execution...")
            print(f"   Task: {task.description}")

            # Execute the task
            result = await agent.execute_task(task, context="Due diligence research")

            print("✅ Task executed successfully")
            print(f"   Task ID: {result['task_id']}")
            print(f"   Confidence: {result['confidence']}")
            print(f"   Citations: {len(result['citations'])} sources")
            print(f"   Results keys: {list(result['results'].keys())}")

        except Exception as e:
            print(f"⚠️ Task execution test failed (expected without API keys): {e}")
    else:
        print("⚠️ Skipping task execution test - OpenAI API key not configured")

    print()
    print("🎉 Research Agent testing completed!")


if __name__ == "__main__":
    asyncio.run(test_research_agent())
