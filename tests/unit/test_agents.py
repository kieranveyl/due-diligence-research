from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.agents.planner import PlanningAgent
from src.agents.supervisor import SupervisorAgent
from src.agents.task_agents.financial import FinancialAgent
from src.agents.task_agents.legal import LegalAgent
from src.agents.task_agents.research import ResearchAgent
from src.agents.task_agents.osint import OSINTAgent
from src.agents.task_agents.verification import VerificationAgent
from src.state.definitions import ResearchTask


@pytest.mark.asyncio
async def test_supervisor_agent_creation():
    """Test supervisor agent creation"""
    with patch('langchain_openai.ChatOpenAI'):
        supervisor = SupervisorAgent()
        agent = supervisor.create_agent()
        assert agent is not None

@pytest.mark.asyncio
async def test_planner_query_analysis():
    """Test planning agent query analysis"""
    with patch('src.agents.planner.ChatOpenAI') as mock_openai:
        # Mock the AI response
        mock_response = MagicMock()
        mock_response.content = '{"complexity": "moderate", "estimated_time": 15, "key_areas": ["background", "compliance"], "risk_level": "medium"}'

        mock_model = AsyncMock()
        mock_model.ainvoke.return_value = mock_response
        mock_openai.return_value = mock_model

        planner = PlanningAgent()
        analysis = await planner._analyze_query("Research XYZ Corp financial status")

        assert "complexity" in analysis
        assert analysis["complexity"] in ["simple", "moderate", "complex"]
        assert "estimated_time" in analysis
        assert isinstance(analysis["estimated_time"], (int, float))

@pytest.mark.asyncio
async def test_financial_agent_creation():
    """Test financial agent creation"""
    with patch('langchain_openai.ChatOpenAI'):
        financial = FinancialAgent()
        agent = financial.create_agent()
        assert agent is not None

@pytest.mark.asyncio
async def test_financial_agent_task_execution():
    """Test financial agent task execution"""
    with patch('langchain_openai.ChatOpenAI'):
        financial = FinancialAgent()

        # Create a sample task
        task = ResearchTask(
            description="Analyze financial status of Tesla Inc",
            assigned_agent="financial",
            output_schema={"financial_summary": "dict", "key_findings": "list"}
        )

        # Execute task
        result = await financial.execute_task(task, "Tesla Inc financial analysis")

        assert "task_id" in result
        assert "results" in result
        assert "citations" in result
        assert "confidence" in result
        assert result["task_id"] == task.id
        assert isinstance(result["confidence"], float)
        assert 0.0 <= result["confidence"] <= 1.0

@pytest.mark.asyncio
async def test_legal_agent_creation():
    """Test legal agent creation"""
    with patch('langchain_openai.ChatOpenAI'):
        legal = LegalAgent()
        agent = legal.create_agent()
        assert agent is not None

@pytest.mark.asyncio
async def test_legal_agent_task_execution():
    """Test legal agent task execution"""
    with patch('langchain_openai.ChatOpenAI'):
        legal = LegalAgent()

        # Create a sample task
        task = ResearchTask(
            description="Legal compliance analysis for Tesla Inc",
            assigned_agent="legal",
            output_schema={"legal_summary": "dict", "risk_factors": "list"}
        )

        # Execute task
        result = await legal.execute_task(task, "Tesla Inc legal compliance review")

        assert "task_id" in result
        assert "results" in result
        assert "citations" in result
        assert "confidence" in result
        assert result["task_id"] == task.id
        assert isinstance(result["confidence"], float)
        assert 0.0 <= result["confidence"] <= 1.0

@pytest.mark.asyncio
async def test_research_agent_creation():
    """Test research agent creation with Exa-first configuration"""
    with patch('langchain_openai.ChatOpenAI'):
        research = ResearchAgent()
        agent = research.create_agent()
        assert agent is not None
        # Should have multiple tools (5 Exa + 1 Tavily, or fallback dummy)
        assert len(research.tools) >= 1


@pytest.mark.asyncio
async def test_research_agent_task_execution():
    """Test research agent task execution"""
    with patch('langchain_openai.ChatOpenAI'):
        research = ResearchAgent()

        # Create a sample task
        task = ResearchTask(
            description="Research Tesla Inc company overview",
            assigned_agent="research",
            output_schema={"findings": "str", "summary": "str"}
        )

        # Execute task
        result = await research.execute_task(task, "Tesla Inc comprehensive research")

        assert "task_id" in result
        assert "results" in result
        assert "citations" in result
        assert "confidence" in result
        assert result["task_id"] == task.id
        assert isinstance(result["confidence"], float)
        assert 0.0 <= result["confidence"] <= 1.0


@pytest.mark.asyncio
async def test_osint_agent_creation():
    """Test OSINT agent creation with comprehensive digital investigation tools"""
    with patch('langchain_openai.ChatOpenAI'):
        osint = OSINTAgent()
        agent = osint.create_agent()
        assert agent is not None
        # Should have multiple tools for OSINT investigation
        assert len(osint.tools) >= 1


@pytest.mark.asyncio
async def test_osint_agent_task_execution():
    """Test OSINT agent task execution"""
    with patch('langchain_openai.ChatOpenAI'):
        osint = OSINTAgent()

        # Create a sample task
        task = ResearchTask(
            description="OSINT investigation of Tesla Inc digital footprint",
            assigned_agent="osint",
            output_schema={"digital_presence": "dict", "reputation_analysis": "dict"}
        )

        # Execute task
        result = await osint.execute_task(task, "Tesla Inc OSINT analysis")

        assert "task_id" in result
        assert "results" in result
        assert "citations" in result
        assert "confidence" in result
        assert result["task_id"] == task.id


@pytest.mark.asyncio
async def test_verification_agent_creation():
    """Test verification agent creation with fact-checking capabilities"""
    with patch('langchain_openai.ChatOpenAI'):
        verification = VerificationAgent()
        agent = verification.create_agent()
        assert agent is not None
        # Should have multiple tools for verification and fact-checking
        assert len(verification.tools) >= 1


@pytest.mark.asyncio
async def test_verification_agent_task_execution():
    """Test verification agent task execution"""
    with patch('langchain_openai.ChatOpenAI'):
        verification = VerificationAgent()

        # Create a sample task
        task = ResearchTask(
            description="Verify financial claims about Tesla Inc",
            assigned_agent="verification",
            output_schema={"verification_results": "dict", "confidence_scores": "dict"}
        )

        # Execute task
        result = await verification.execute_task(task, "Tesla Inc fact verification")

        assert "task_id" in result
        assert "results" in result
        assert "citations" in result
        assert "confidence" in result
        assert result["task_id"] == task.id
