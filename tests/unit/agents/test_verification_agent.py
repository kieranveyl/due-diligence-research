#!/usr/bin/env python3
"""
Test script for the Verification Agent with LangChain integrations
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.agents.task_agents.verification import VerificationAgent
from src.config.settings import settings
from src.state.definitions import ResearchTask


async def test_verification_agent():
    """Test the Verification Agent initialization and tool setup"""
    
    print("✅ Testing Verification Agent v2.0 with LangChain integrations...")
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
        agent = VerificationAgent()
        print("✅ Verification Agent initialized successfully")
        print(f"   Model: {agent.model_name}")
        print(f"   Tools available: {len(agent.tools)}")
        for i, tool in enumerate(agent.tools):
            print(f"   {i+1}. {tool.name}: {tool.description}")
    except Exception as e:
        print(f"❌ Failed to initialize Verification Agent: {e}")
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
        print("✅ LangGraph verification agent created successfully")
        print(f"   Agent name: verification_agent")
    except Exception as e:
        print(f"❌ Failed to create LangGraph verification agent: {e}")
        return
    
    print()
    
    # Test 4: Mock task execution
    try:
        # Create a verification task
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
        
        print("✅ Testing verification task execution...")
        print(f"   Task: {task.description}")
        
        # Execute the task
        result = await agent.execute_task(task, context="Due diligence fact verification")
        
        print("✅ Verification task executed successfully")
        print(f"   Task ID: {result['task_id']}")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Citations: {len(result['citations'])} sources")
        print(f"   Results keys: {list(result['results'].keys())}")
        
    except Exception as e:
        print(f"⚠️ Verification task execution test failed (expected without API keys): {e}")
    
    print()
    print("🎉 Verification Agent testing completed!")


if __name__ == "__main__":
    asyncio.run(test_verification_agent())