import pytest

from src.workflows.due_diligence import DueDiligenceWorkflow


@pytest.mark.asyncio
async def test_workflow_initialization():
    """Test workflow can be initialized"""
    workflow = DueDiligenceWorkflow()
    assert workflow.compiled is not None

@pytest.mark.asyncio
async def test_simple_research_flow(workflow, sample_request):
    """Test basic research workflow"""

    events = []
    async for event in workflow.run(
        query=sample_request["query"],
        entity_type=sample_request["entity_type"],
        entity_name=sample_request["entity_name"]
    ):
        events.append(event)
        # Limit events for testing
        if len(events) >= 3:
            break

    assert len(events) > 0
    # Add more specific assertions based on expected flow
