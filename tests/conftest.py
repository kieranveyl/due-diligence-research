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

    # Create mock tool classes that inherit from BaseTool
    class MockExaTool(BaseTool):
        name = "exa_search"
        description = "Mock Exa search tool"

        def _run(self, query: str) -> str:
            return "Mock exa results"

    with patch('src.agents.task_agents.research.ExaSearchResults') as mock_exa, \
         patch('langchain_openai.ChatOpenAI') as mock_openai:

        # Mock the tools to return proper BaseTool instances
        mock_exa.return_value = MockExaTool()

        # Mock the OpenAI model
        mock_model = MagicMock()
        mock_openai.return_value = mock_model

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
