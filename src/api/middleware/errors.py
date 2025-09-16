import structlog
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

logger = structlog.get_logger()

async def error_handling_middleware(request: Request, call_next):
    """Global error handling middleware"""

    try:
        response = await call_next(request)
        return response

    except HTTPException as e:
        logger.warning(
            "http_exception",
            status_code=e.status_code,
            detail=e.detail,
            url=str(request.url)
        )
        raise

    except Exception as e:
        logger.error(
            "unhandled_exception",
            error=str(e),
            url=str(request.url),
            exc_info=True
        )

        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred"
            }
        )
