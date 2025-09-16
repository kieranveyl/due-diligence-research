import asyncio
import os
from unittest.mock import MagicMock, patch

import pytest

from src.workflows.due_diligence import DueDiligenceWorkflow


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
def mock_api_keys():
    """Mock API keys for testing"""
    with patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test-openai-key',
        'ANTHROPIC_API_KEY': 'test-anthropic-key',
        'EXA_API_KEY': 'test-exa-key',
        'LANGSMITH_API_KEY': 'test-langsmith-key',
        'POSTGRES_URL': 'sqlite:///test.db',
        'REDIS_URL': 'redis://localhost:6379/1'
    }):
        yield

@pytest.fixture
def workflow():
    """Create workflow instance for testing"""
    from langchain_core.tools import BaseTool
    from langchain_core.messages import AIMessage

    # Create mock tool classes that inherit from BaseTool
    class MockExaTool(BaseTool):
        name: str = "exa_search"
        description: str = "Mock Exa search tool"

        def _run(self, query: str) -> str:
            return "Mock exa results"

    with patch('src.agents.task_agents.research.ExaSearchResults') as mock_exa, \
         patch('src.agents.task_agents.financial.ExaSearchResults') as mock_exa_financial, \
         patch('src.agents.task_agents.legal.ExaSearchResults') as mock_exa_legal, \
         patch('src.agents.task_agents.osint.ExaSearchResults') as mock_exa_osint, \
         patch('src.agents.task_agents.verification.ExaSearchResults') as mock_exa_verification, \
         patch('langchain_openai.ChatOpenAI') as mock_openai, \
         patch('src.state.checkpointer.checkpointer_factory.create_checkpointer') as mock_checkpointer:

        # Mock the tools to return proper BaseTool instances
        mock_exa.return_value = MockExaTool()
        mock_exa_financial.return_value = MockExaTool()
        mock_exa_legal.return_value = MockExaTool()
        mock_exa_osint.return_value = MockExaTool()
        mock_exa_verification.return_value = MockExaTool()

        # Mock the OpenAI model with proper async methods
        async def mock_ainvoke(*args, **kwargs):
            return AIMessage(content="Mock response")
        
        mock_model = MagicMock()
        mock_model.ainvoke = mock_ainvoke
        mock_model.invoke = MagicMock(return_value=AIMessage(content="Mock response"))
        mock_openai.return_value = mock_model

        # Mock the checkpointer
        mock_checkpointer_instance = MagicMock()
        mock_checkpointer.return_value = mock_checkpointer_instance

        wf = DueDiligenceWorkflow()
        return wf

@pytest.fixture
def sample_request():
    """Sample research request"""
    return {
        "query": "Research ABC Corp for potential acquisition",
        "entity_type": "company",
        "entity_name": "ABC Corp"
    }
