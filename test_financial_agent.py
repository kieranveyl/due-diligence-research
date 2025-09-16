#!/usr/bin/env python3
"""
Test script for the Financial Agent with LangChain integrations
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.agents.task_agents.financial import FinancialAgent
from src.config.settings import settings
from src.state.definitions import ResearchTask


async def test_financial_agent():
    """Test the Financial Agent initialization and tool setup"""
    
    print("💰 Testing Financial Agent v2.0 with LangChain integrations...")
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
        agent = FinancialAgent()
        print("✅ Financial Agent initialized successfully")
        print(f"   Model: {agent.model_name}")
        print(f"   Tools available: {len(agent.tools)}")
        for i, tool in enumerate(agent.tools):
            print(f"   {i+1}. {tool.name}: {tool.description}")
    except Exception as e:
        print(f"❌ Failed to initialize Financial Agent: {e}")
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
        print("✅ LangGraph financial agent created successfully")
        print(f"   Agent name: financial_agent")
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
        
    except Exception as e:
        print(f"⚠️ Financial task execution test failed (expected without API keys): {e}")
    
    print()
    print("🎉 Financial Agent testing completed!")


if __name__ == "__main__":
    asyncio.run(test_financial_agent())