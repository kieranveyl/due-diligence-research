#!/usr/bin/env python3
"""
Test script for the OSINT Agent with LangChain integrations
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.agents.task_agents.osint import OSINTAgent
from src.state.definitions import ResearchTask


async def test_osint_agent():
    """Test the OSINT Agent initialization and tool setup"""

    print("🔍 Testing OSINT Agent v2.0 with LangChain integrations...")
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
        agent = OSINTAgent()
        print("✅ OSINT Agent initialized successfully")
        print(f"   Model: {agent.model_name}")
        print(f"   Tools available: {len(agent.tools)}")
        for i, tool in enumerate(agent.tools):
            print(f"   {i+1}. {tool.name}: {tool.description}")
    except Exception as e:
        print(f"❌ Failed to initialize OSINT Agent: {e}")
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
        print("✅ LangGraph OSINT agent created successfully")
        print("   Agent name: osint_agent")
    except Exception as e:
        print(f"❌ Failed to create LangGraph OSINT agent: {e}")
        return

    print()

    # Test 4: Mock task execution
    try:
        # Create an OSINT investigation task
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

        print("🔍 Testing OSINT task execution...")
        print(f"   Task: {task.description}")

        # Execute the task
        result = await agent.execute_task(task, context="Due diligence OSINT investigation")

        print("✅ OSINT task executed successfully")
        print(f"   Task ID: {result['task_id']}")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Citations: {len(result['citations'])} sources")
        print(f"   Results keys: {list(result['results'].keys())}")

    except Exception as e:
        print(f"⚠️ OSINT task execution test failed (expected without API keys): {e}")

    print()
    print("🎉 OSINT Agent testing completed!")


if __name__ == "__main__":
    asyncio.run(test_osint_agent())
