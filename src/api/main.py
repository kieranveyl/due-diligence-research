import json
import uuid
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from src.config.settings import settings
from src.workflows.due_diligence import DueDiligenceWorkflow

def _make_serializable(obj):
    """Convert complex objects to JSON-serializable format"""
    from enum import Enum
    
    if hasattr(obj, 'dict'):
        return obj.dict()
    elif isinstance(obj, Enum):
        return obj.value
    elif hasattr(obj, '__dict__'):
        result = {}
        for key, value in obj.__dict__.items():
            try:
                result[key] = _make_serializable(value)
            except (TypeError, ValueError):
                result[key] = str(value)
        return result
    elif isinstance(obj, dict):
        return {key: _make_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_make_serializable(item) for item in obj]
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    else:
        return str(obj)

# Global workflow instance
workflow = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global workflow
    workflow = DueDiligenceWorkflow()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Due Diligence API",
    description="Multi-Agent Due Diligence Research System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
from pydantic import BaseModel


class ResearchRequest(BaseModel):
    query: str
    entity_type: str = "company"
    entity_name: str
    thread_id: str | None = None

class ResearchResponse(BaseModel):
    thread_id: str
    status: str
    stream_url: str

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/research", response_model=ResearchResponse)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """Start new due diligence research"""

    thread_id = request.thread_id or str(uuid.uuid4())

    return ResearchResponse(
        thread_id=thread_id,
        status="started",
        stream_url=f"/research/{thread_id}/stream"
    )

@app.get("/research/{thread_id}/stream")
async def stream_results(thread_id: str):
    """Stream research results as they become available"""

    async def event_generator():
        try:
            # This would typically come from the request body
            # For demo, we'll use placeholder values
            async for event in workflow.run(
                query="Sample query",
                entity_type="company",
                entity_name="Sample Corp",
                thread_id=thread_id
            ):
                # Format as Server-Sent Events
                # Convert complex objects to JSON-serializable format
                serializable_event = _make_serializable(event)
                event_data = json.dumps(serializable_event)
                yield f"data: {event_data}\n\n"
        except Exception as e:
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.get("/research/{thread_id}/status")
async def get_research_status(thread_id: str):
    """Get current status of research"""
    # Implementation would check checkpointer for thread status
    return {"thread_id": thread_id, "status": "running"}

@app.get("/debug/workflow")
async def debug_workflow():
    """Debug endpoint to test workflow initialization"""
    try:
        # Test workflow creation
        test_workflow = workflow
        if test_workflow is None:
            return {"error": "Workflow not initialized"}
        
        # Test checkpointer
        checkpointer = await test_workflow._ensure_compiled()
        
        return {
            "status": "success",
            "workflow_initialized": test_workflow is not None,
            "checkpointer_type": str(type(test_workflow.checkpointer)),
            "compiled": test_workflow.compiled is not None
        }
    except Exception as e:
        return {"error": str(e), "type": str(type(e))}

@app.get("/debug/simple-run")
async def debug_simple_run():
    """Debug endpoint to test simple workflow execution"""
    try:
        import uuid
        thread_id = str(uuid.uuid4())
        
        # Test basic state creation
        initial_state = {
            "messages": [],
            "query": "Test query",
            "entity_type": "company",
            "entity_name": "Test Corp",
            "tasks": [],
            "research_plan": "",
            "raw_findings": {},
            "synthesized_report": "",
            "citations": [],
            "confidence_scores": {},
            "thread_id": thread_id,
            "session_id": thread_id,
            "user_id": None,
            "metadata": {},
            "ready_for_synthesis": False,
            "human_feedback_required": False,
            "completed": False
        }
        
        config = {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": "due_diligence"
            }
        }
        
        # Test just one step
        compiled_graph = await workflow._ensure_compiled()
        result = await compiled_graph.ainvoke(initial_state, config=config)
        
        return {
            "status": "success",
            "thread_id": thread_id,
            "result_keys": list(result.keys()) if result else [],
            "completed": result.get("completed", False) if result else False
        }
        
    except Exception as e:
        import traceback
        return {
            "error": str(e), 
            "type": str(type(e)),
            "traceback": traceback.format_exc()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.environment == "development",
        log_level=settings.log_level.lower()
    )
