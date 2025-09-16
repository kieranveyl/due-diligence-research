"""
Audit Logging and Security Event Tracking
"""

import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from enum import Enum

import structlog
from structlog.stdlib import LoggerFactory

from src.config.settings import settings


class SecurityEventType(Enum):
    """Types of security events to track"""
    SESSION_CREATED = "session_created"
    SESSION_ACCESSED = "session_accessed"
    SESSION_MODIFIED = "session_modified"
    SESSION_DELETED = "session_deleted"
    CREDENTIAL_ADDED = "credential_added"
    CREDENTIAL_ACCESSED = "credential_accessed"
    CREDENTIAL_DELETED = "credential_deleted"
    API_KEY_USED = "api_key_used"
    ENCRYPTION_KEY_ROTATED = "encryption_key_rotated"
    AUTHENTICATION_FAILED = "authentication_failed"
    DATA_EXPORT = "data_export"
    SYSTEM_ACCESS = "system_access"
    ERROR_OCCURRED = "error_occurred"


class AuditLogger:
    """Structured audit logging for compliance and security"""
    
    def __init__(self):
        self.setup_structured_logging()
        self.logger = structlog.get_logger("audit")
        self.log_dir = self._ensure_log_directory()
    
    def setup_structured_logging(self):
        """Configure structlog for structured audit logging"""
        
        # Configure structlog processors
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    
    def _ensure_log_directory(self) -> Path:
        """Ensure audit log directory exists"""
        log_dir = Path.home() / ".config" / "due-diligence" / "audit-logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir
    
    async def log_security_event(
        self,
        event_type: SecurityEventType,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        success: bool = True,
        error_message: Optional[str] = None
    ):
        """Log a security event with full context"""
        
        event_data = {
            "event_type": event_type.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id or "system",
            "session_id": session_id,
            "resource_id": resource_id,
            "success": success,
            "error_message": error_message,
            "details": details or {},
            "source": "due_diligence_v2"
        }
        
        # Log to structured logger
        if success:
            self.logger.info(
                "Security event logged",
                **event_data
            )
        else:
            self.logger.warning(
                "Security event failed",
                **event_data
            )
        
        # Also save to daily audit file
        await self._write_audit_file(event_data)
    
    async def _write_audit_file(self, event_data: Dict[str, Any]):
        """Write audit event to daily file"""
        today = datetime.now().strftime("%Y-%m-%d")
        audit_file = self.log_dir / f"audit-{today}.jsonl"
        
        try:
            with open(audit_file, "a") as f:
                f.write(json.dumps(event_data) + "\n")
        except Exception as e:
            # Use fallback logger if audit file write fails
            self.logger.error("Failed to write audit file", error=str(e))
    
    async def log_session_event(
        self,
        event_type: SecurityEventType,
        session_id: str,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """Log session-related security event"""
        await self.log_security_event(
            event_type=event_type,
            user_id=user_id,
            session_id=session_id,
            resource_id=session_id,
            details=details
        )
    
    async def log_credential_event(
        self,
        event_type: SecurityEventType,
        service: str,
        credential_type: str,
        user_id: Optional[str] = None,
        success: bool = True
    ):
        """Log credential-related security event"""
        await self.log_security_event(
            event_type=event_type,
            user_id=user_id,
            resource_id=f"{service}:{credential_type}",
            details={
                "service": service,
                "credential_type": credential_type
            },
            success=success
        )
    
    async def log_api_usage(
        self,
        service: str,
        endpoint: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        response_size: Optional[int] = None,
        duration_ms: Optional[float] = None,
        success: bool = True,
        error_code: Optional[str] = None
    ):
        """Log API usage for audit trail"""
        await self.log_security_event(
            event_type=SecurityEventType.API_KEY_USED,
            user_id=user_id,
            session_id=session_id,
            resource_id=f"{service}:{endpoint}",
            details={
                "service": service,
                "endpoint": endpoint,
                "response_size_bytes": response_size,
                "duration_ms": duration_ms,
                "error_code": error_code
            },
            success=success
        )
    
    async def search_audit_logs(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        event_types: Optional[List[SecurityEventType]] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Search audit logs with filters"""
        
        results = []
        
        # Determine date range
        if not start_date:
            start_date = datetime.now() - timedelta(days=7)  # Default last 7 days
        if not end_date:
            end_date = datetime.now()
        
        # Search through daily audit files
        current_date = start_date.date()
        while current_date <= end_date.date() and len(results) < limit:
            audit_file = self.log_dir / f"audit-{current_date.strftime('%Y-%m-%d')}.jsonl"
            
            if audit_file.exists():
                with open(audit_file, "r") as f:
                    for line in f:
                        if len(results) >= limit:
                            break
                        
                        try:
                            event = json.loads(line.strip())
                            
                            # Apply filters
                            if event_types and event.get("event_type") not in [et.value for et in event_types]:
                                continue
                            if user_id and event.get("user_id") != user_id:
                                continue
                            if session_id and event.get("session_id") != session_id:
                                continue
                            
                            # Check timestamp within range
                            event_time = datetime.fromisoformat(event.get("timestamp", ""))
                            if start_date <= event_time <= end_date:
                                results.append(event)
                        
                        except (json.JSONDecodeError, ValueError):
                            continue
            
            current_date += timedelta(days=1)
        
        return results[-limit:]  # Return most recent results
    
    async def cleanup_old_logs(self, retention_days: int = None):
        """Clean up audit logs older than retention period"""
        if retention_days is None:
            retention_days = getattr(settings, 'audit_log_retention_days', 90)
        
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        deleted_count = 0
        
        for log_file in self.log_dir.glob("audit-*.jsonl"):
            try:
                # Extract date from filename
                date_str = log_file.stem.replace("audit-", "")
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
                
                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    
            except (ValueError, OSError) as e:
                self.logger.warning(f"Failed to process log file {log_file}: {e}")
        
        if deleted_count > 0:
            await self.log_security_event(
                event_type=SecurityEventType.SYSTEM_ACCESS,
                details={
                    "action": "log_cleanup",
                    "files_deleted": deleted_count,
                    "retention_days": retention_days
                }
            )


class SecurityEventLogger:
    """High-level security event logging interface"""
    
    def __init__(self):
        self.audit_logger = AuditLogger()
    
    async def log_research_session_start(
        self,
        session_id: str,
        entity_name: str,
        user_id: Optional[str] = None,
        scope: Optional[List[str]] = None
    ):
        """Log the start of a research session"""
        await self.audit_logger.log_session_event(
            event_type=SecurityEventType.SESSION_CREATED,
            session_id=session_id,
            user_id=user_id,
            details={
                "entity_name": entity_name,
                "research_scope": scope or [],
                "action": "research_session_started"
            }
        )
    
    async def log_research_session_complete(
        self,
        session_id: str,
        duration_seconds: float,
        confidence_score: float,
        sources_count: int,
        user_id: Optional[str] = None
    ):
        """Log the completion of a research session"""
        await self.audit_logger.log_session_event(
            event_type=SecurityEventType.SESSION_MODIFIED,
            session_id=session_id,
            user_id=user_id,
            details={
                "action": "research_session_completed",
                "duration_seconds": duration_seconds,
                "confidence_score": confidence_score,
                "sources_count": sources_count
            }
        )
    
    async def log_data_export(
        self,
        session_id: str,
        export_format: str,
        file_path: Optional[str] = None,
        user_id: Optional[str] = None
    ):
        """Log data export events"""
        await self.audit_logger.log_security_event(
            event_type=SecurityEventType.DATA_EXPORT,
            user_id=user_id,
            session_id=session_id,
            resource_id=file_path,
            details={
                "export_format": export_format,
                "file_path": file_path,
                "action": "data_exported"
            }
        )
    
    async def log_error_event(
        self,
        error_type: str,
        error_message: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """Log error events for security monitoring"""
        await self.audit_logger.log_security_event(
            event_type=SecurityEventType.ERROR_OCCURRED,
            user_id=user_id,
            session_id=session_id,
            success=False,
            error_message=error_message,
            details={
                "error_type": error_type,
                **(details or {})
            }
        )