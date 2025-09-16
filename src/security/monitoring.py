"""
Security Monitoring and Real-time Event Detection
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Callable, Any
from dataclasses import dataclass
from collections import defaultdict, deque

from .audit import SecurityEventType, AuditLogger


@dataclass
class SecurityAlert:
    """Security alert data structure"""
    alert_id: str
    alert_type: str
    severity: str  # critical, high, medium, low
    message: str
    timestamp: datetime
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class SecurityMetrics:
    """Security metrics tracking"""
    
    def __init__(self):
        self.reset_counters()
    
    def reset_counters(self):
        """Reset all metric counters"""
        self.events_by_type = defaultdict(int)
        self.failed_attempts = defaultdict(int)
        self.api_usage_count = defaultdict(int)
        self.session_activity = defaultdict(int)
        self.error_rates = defaultdict(list)
        self.last_reset = datetime.now()
    
    def record_event(self, event_type: SecurityEventType, success: bool = True):
        """Record a security event for metrics"""
        self.events_by_type[event_type.value] += 1
        
        if not success:
            self.failed_attempts[event_type.value] += 1
    
    def record_api_usage(self, service: str, endpoint: str, success: bool = True):
        """Record API usage for rate limiting and monitoring"""
        key = f"{service}:{endpoint}"
        self.api_usage_count[key] += 1
        
        if not success:
            self.error_rates[key].append(datetime.now())
    
    def get_error_rate(self, service: str, endpoint: str, window_minutes: int = 5) -> float:
        """Calculate error rate for service/endpoint in time window"""
        key = f"{service}:{endpoint}"
        cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
        
        # Clean old errors
        self.error_rates[key] = [
            error_time for error_time in self.error_rates[key]
            if error_time > cutoff_time
        ]
        
        total_requests = self.api_usage_count[key]
        error_count = len(self.error_rates[key])
        
        return error_count / max(total_requests, 1)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of security metrics"""
        return {
            "events_by_type": dict(self.events_by_type),
            "failed_attempts": dict(self.failed_attempts),
            "api_usage": dict(self.api_usage_count),
            "session_activity": dict(self.session_activity),
            "uptime_seconds": (datetime.now() - self.last_reset).total_seconds()
        }


class SecurityMonitor:
    """Real-time security monitoring and alerting"""
    
    def __init__(self):
        self.audit_logger = AuditLogger()
        self.metrics = SecurityMetrics()
        self.alerts: deque = deque(maxlen=1000)  # Keep last 1000 alerts
        self.alert_handlers: List[Callable[[SecurityAlert], None]] = []
        self.monitoring_active = False
        
        # Security thresholds
        self.thresholds = {
            "max_failed_logins_per_hour": 10,
            "max_api_errors_per_minute": 5,
            "max_sessions_per_user": 20,
            "suspicious_activity_threshold": 0.1,
            "credential_access_rate_limit": 30  # per hour
        }
        
        # Rate limiting windows
        self.rate_windows = {
            "failed_logins": deque(maxlen=100),
            "credential_access": deque(maxlen=100),
            "session_creation": deque(maxlen=100)
        }
    
    async def start_monitoring(self):
        """Start security monitoring background task"""
        self.monitoring_active = True
        
        # Start background monitoring tasks
        monitoring_tasks = [
            self._monitor_failed_attempts(),
            self._monitor_api_error_rates(),
            self._monitor_session_activity(),
            self._cleanup_old_data()
        ]
        
        await asyncio.gather(*monitoring_tasks)
    
    def stop_monitoring(self):
        """Stop security monitoring"""
        self.monitoring_active = False
    
    def add_alert_handler(self, handler: Callable[[SecurityAlert], None]):
        """Add custom alert handler"""
        self.alert_handlers.append(handler)
    
    async def check_security_event(
        self,
        event_type: SecurityEventType,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        success: bool = True,
        details: Optional[Dict[str, Any]] = None
    ):
        """Check security event and trigger alerts if needed"""
        
        # Record metrics
        self.metrics.record_event(event_type, success)
        
        # Check for suspicious patterns
        alerts = []
        
        if not success:
            # Failed event - check for abuse patterns
            if event_type == SecurityEventType.AUTHENTICATION_FAILED:
                alerts.extend(await self._check_failed_login_abuse(user_id))
            
            elif event_type == SecurityEventType.CREDENTIAL_ACCESSED:
                alerts.extend(await self._check_credential_access_abuse(user_id))
        
        # Check for unusual session activity
        if event_type in [SecurityEventType.SESSION_CREATED, SecurityEventType.SESSION_ACCESSED]:
            alerts.extend(await self._check_session_abuse(user_id, session_id))
        
        # Process any alerts
        for alert in alerts:
            await self._handle_alert(alert)
    
    async def _check_failed_login_abuse(self, user_id: Optional[str]) -> List[SecurityAlert]:
        """Check for failed login abuse patterns"""
        alerts = []
        
        # Add to rate limiting window
        self.rate_windows["failed_logins"].append({
            "timestamp": datetime.now(),
            "user_id": user_id
        })
        
        # Check recent failed logins for this user
        recent_failures = [
            event for event in self.rate_windows["failed_logins"]
            if event["user_id"] == user_id and
            event["timestamp"] > datetime.now() - timedelta(hours=1)
        ]
        
        if len(recent_failures) >= self.thresholds["max_failed_logins_per_hour"]:
            alerts.append(SecurityAlert(
                alert_id=f"failed_login_abuse_{user_id}_{int(time.time())}",
                alert_type="authentication_abuse",
                severity="high",
                message=f"User {user_id} exceeded failed login threshold",
                timestamp=datetime.now(),
                user_id=user_id,
                details={"failed_attempts": len(recent_failures)}
            ))
        
        return alerts
    
    async def _check_credential_access_abuse(self, user_id: Optional[str]) -> List[SecurityAlert]:
        """Check for credential access abuse"""
        alerts = []
        
        # Add to rate limiting window
        self.rate_windows["credential_access"].append({
            "timestamp": datetime.now(),
            "user_id": user_id
        })
        
        # Check recent credential accesses
        recent_accesses = [
            event for event in self.rate_windows["credential_access"]
            if event["user_id"] == user_id and
            event["timestamp"] > datetime.now() - timedelta(hours=1)
        ]
        
        if len(recent_accesses) >= self.thresholds["credential_access_rate_limit"]:
            alerts.append(SecurityAlert(
                alert_id=f"credential_abuse_{user_id}_{int(time.time())}",
                alert_type="credential_abuse",
                severity="medium",
                message=f"User {user_id} exceeded credential access rate limit",
                timestamp=datetime.now(),
                user_id=user_id,
                details={"access_count": len(recent_accesses)}
            ))
        
        return alerts
    
    async def _check_session_abuse(
        self,
        user_id: Optional[str],
        session_id: Optional[str]
    ) -> List[SecurityAlert]:
        """Check for session creation abuse"""
        alerts = []
        
        # Add to rate limiting window
        self.rate_windows["session_creation"].append({
            "timestamp": datetime.now(),
            "user_id": user_id,
            "session_id": session_id
        })
        
        # Check for too many active sessions
        recent_sessions = [
            event for event in self.rate_windows["session_creation"]
            if event["user_id"] == user_id and
            event["timestamp"] > datetime.now() - timedelta(hours=24)
        ]
        
        if len(recent_sessions) >= self.thresholds["max_sessions_per_user"]:
            alerts.append(SecurityAlert(
                alert_id=f"session_abuse_{user_id}_{int(time.time())}",
                alert_type="session_abuse",
                severity="medium",
                message=f"User {user_id} created too many sessions",
                timestamp=datetime.now(),
                user_id=user_id,
                details={"session_count": len(recent_sessions)}
            ))
        
        return alerts
    
    async def _handle_alert(self, alert: SecurityAlert):
        """Handle security alert"""
        # Store alert
        self.alerts.append(alert)
        
        # Log to audit system
        await self.audit_logger.log_security_event(
            event_type=SecurityEventType.SYSTEM_ACCESS,
            user_id=alert.user_id,
            session_id=alert.session_id,
            details={
                "alert_type": alert.alert_type,
                "severity": alert.severity,
                "message": alert.message,
                "alert_id": alert.alert_id,
                **(alert.details or {})
            }
        )
        
        # Call custom alert handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                # Don't let handler errors break monitoring
                print(f"Alert handler error: {e}")
    
    async def _monitor_failed_attempts(self):
        """Background monitoring for failed attempts"""
        while self.monitoring_active:
            try:
                # Clean old entries from rate windows
                cutoff_time = datetime.now() - timedelta(hours=1)
                
                for window_name, window in self.rate_windows.items():
                    # Remove old entries
                    while window and window[0]["timestamp"] < cutoff_time:
                        window.popleft()
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                print(f"Failed attempts monitoring error: {e}")
                await asyncio.sleep(60)
    
    async def _monitor_api_error_rates(self):
        """Background monitoring for API error rates"""
        while self.monitoring_active:
            try:
                # Check error rates for all services
                for service_endpoint, usage_count in self.metrics.api_usage_count.items():
                    error_rate = self.metrics.get_error_rate(
                        service_endpoint.split(":")[0],
                        service_endpoint.split(":")[1]
                    )
                    
                    if error_rate > 0.5:  # 50% error rate
                        await self._handle_alert(SecurityAlert(
                            alert_id=f"api_error_rate_{service_endpoint}_{int(time.time())}",
                            alert_type="api_error_rate",
                            severity="high",
                            message=f"High error rate for {service_endpoint}: {error_rate:.1%}",
                            timestamp=datetime.now(),
                            details={
                                "service_endpoint": service_endpoint,
                                "error_rate": error_rate,
                                "usage_count": usage_count
                            }
                        ))
                
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                print(f"API error rate monitoring error: {e}")
                await asyncio.sleep(300)
    
    async def _monitor_session_activity(self):
        """Background monitoring for session activity"""
        while self.monitoring_active:
            try:
                # Monitor for unusual session patterns
                # This could include geolocation analysis, time-based patterns, etc.
                
                await asyncio.sleep(600)  # Check every 10 minutes
                
            except Exception as e:
                print(f"Session activity monitoring error: {e}")
                await asyncio.sleep(600)
    
    async def _cleanup_old_data(self):
        """Clean up old monitoring data"""
        while self.monitoring_active:
            try:
                # Clean metrics older than 24 hours
                if (datetime.now() - self.metrics.last_reset).total_seconds() > 86400:
                    self.metrics.reset_counters()
                
                # Clean old alerts (keep only last 1000, but deque handles this automatically)
                
                await asyncio.sleep(3600)  # Cleanup every hour
                
            except Exception as e:
                print(f"Cleanup error: {e}")
                await asyncio.sleep(3600)
    
    def get_recent_alerts(self, limit: int = 50) -> List[SecurityAlert]:
        """Get recent security alerts"""
        return list(self.alerts)[-limit:]
    
    def get_security_summary(self) -> Dict[str, Any]:
        """Get comprehensive security summary"""
        recent_alerts = self.get_recent_alerts(10)
        
        return {
            "monitoring_active": self.monitoring_active,
            "metrics": self.metrics.get_summary(),
            "recent_alerts": [
                {
                    "alert_id": alert.alert_id,
                    "alert_type": alert.alert_type,
                    "severity": alert.severity,
                    "message": alert.message,
                    "timestamp": alert.timestamp.isoformat()
                }
                for alert in recent_alerts
            ],
            "alert_counts_by_severity": {
                "critical": len([a for a in recent_alerts if a.severity == "critical"]),
                "high": len([a for a in recent_alerts if a.severity == "high"]),
                "medium": len([a for a in recent_alerts if a.severity == "medium"]),
                "low": len([a for a in recent_alerts if a.severity == "low"])
            },
            "thresholds": self.thresholds
        }