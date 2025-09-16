import time

import structlog
from fastapi import Request
from prometheus_client import Counter, Histogram

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

logger = structlog.get_logger()

async def monitoring_middleware(request: Request, call_next):
    """Monitoring middleware for metrics and logging"""

    start_time = time.time()

    # Log request
    logger.info(
        "request_started",
        method=request.method,
        url=str(request.url),
        user_agent=request.headers.get("user-agent", "")
    )

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration = time.time() - start_time

    # Update metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    REQUEST_DURATION.observe(duration)

    # Log response
    logger.info(
        "request_completed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        duration=duration
    )

    return response
