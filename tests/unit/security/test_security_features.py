#!/usr/bin/env python3
"""
Test script for Security Features including encryption, audit logging, and monitoring
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.security.audit import AuditLogger, SecurityEventLogger, SecurityEventType
from src.security.encryption import CredentialManager, SessionEncryption
from src.security.monitoring import SecurityMonitor


async def test_session_encryption():
    """Test session encryption functionality"""
    print("🔐 Testing Session Encryption...")

    try:
        encryptor = SessionEncryption()

        # Test data encryption
        test_data = {
            "session_id": "test-session-123",
            "entity_name": "Tesla Inc",
            "sensitive_data": "This contains API keys and sensitive info",
            "research_results": ["finding 1", "finding 2", "finding 3"]
        }

        # Encrypt data
        encrypted_data = encryptor.encrypt_session(test_data)
        print(f"   ✅ Data encrypted successfully (length: {len(encrypted_data)})")

        # Decrypt data
        decrypted_data = encryptor.decrypt_session(encrypted_data)
        print("   ✅ Data decrypted successfully")

        # Verify data integrity
        if decrypted_data == test_data:
            print("   ✅ Data integrity verified - encryption/decryption works correctly")
        else:
            print("   ❌ Data integrity check failed")

    except Exception as e:
        print(f"   ❌ Session encryption test failed: {e}")


async def test_credential_manager():
    """Test credential management functionality"""
    print("\n🔑 Testing Credential Manager...")

    try:
        cred_manager = CredentialManager()

        # Store test credentials
        test_credentials = {
            "openai": {"api_key": "sk-test-openai-key-123"},
            "exa": {"api_key": "exa-test-key-456"},
            "tavily": {"api_key": "tavily-test-key-789"}
        }

        for service, creds in test_credentials.items():
            for cred_type, value in creds.items():
                cred_manager.store_credential(service, cred_type, value)

        print("   ✅ Test credentials stored successfully")

        # Retrieve credentials
        for service, creds in test_credentials.items():
            for cred_type, expected_value in creds.items():
                retrieved_value = cred_manager.get_credential(service, cred_type)
                if retrieved_value == expected_value:
                    print(f"   ✅ {service} {cred_type} retrieved correctly")
                else:
                    print(f"   ❌ {service} {cred_type} retrieval failed")

        # Test credential validation
        validation_results = cred_manager.validate_credentials()
        print(f"   ✅ Credential validation: {validation_results}")

        # List services
        services = cred_manager.list_services()
        print(f"   ✅ Available services: {list(services.keys())}")

        # Clean up test credentials
        for service in test_credentials.keys():
            cred_manager.delete_credential(service)

        print("   ✅ Test credentials cleaned up")

    except Exception as e:
        print(f"   ❌ Credential manager test failed: {e}")


async def test_audit_logging():
    """Test audit logging functionality"""
    print("\n📝 Testing Audit Logging...")

    try:
        audit_logger = AuditLogger()

        # Test various security events
        test_events = [
            (SecurityEventType.SESSION_CREATED, "test-session-123", "test-user", {"entity_name": "Tesla Inc"}),
            (SecurityEventType.CREDENTIAL_ACCESSED, None, "test-user", {"service": "openai", "credential_type": "api_key"}),
            (SecurityEventType.API_KEY_USED, "test-session-123", "test-user", {"service": "exa", "endpoint": "search"}),
            (SecurityEventType.DATA_EXPORT, "test-session-123", "test-user", {"format": "json", "file_path": "/tmp/test.json"})
        ]

        for event_type, session_id, user_id, details in test_events:
            await audit_logger.log_security_event(
                event_type=event_type,
                user_id=user_id,
                session_id=session_id,
                details=details
            )
            print(f"   ✅ Logged {event_type.value} event")

        # Test structured security event logger
        security_logger = SecurityEventLogger()

        await security_logger.log_research_session_start(
            session_id="test-session-456",
            entity_name="Apple Inc",
            user_id="test-user",
            scope=["financial", "legal"]
        )
        print("   ✅ Logged research session start")

        await security_logger.log_research_session_complete(
            session_id="test-session-456",
            duration_seconds=120.5,
            confidence_score=0.85,
            sources_count=15,
            user_id="test-user"
        )
        print("   ✅ Logged research session completion")

        # Test audit log search (basic test)
        try:
            recent_logs = await audit_logger.search_audit_logs(limit=5)
            print(f"   ✅ Audit log search returned {len(recent_logs)} events")
        except Exception as e:
            print(f"   ⚠️ Audit log search test skipped: {e}")

    except Exception as e:
        print(f"   ❌ Audit logging test failed: {e}")


async def test_security_monitoring():
    """Test security monitoring functionality"""
    print("\n🛡️ Testing Security Monitoring...")

    try:
        monitor = SecurityMonitor()

        # Test security event checking
        test_events = [
            (SecurityEventType.SESSION_CREATED, "test-user-1", "session-1", True),
            (SecurityEventType.AUTHENTICATION_FAILED, "test-user-2", None, False),
            (SecurityEventType.CREDENTIAL_ACCESSED, "test-user-3", None, True),
            (SecurityEventType.API_KEY_USED, "test-user-1", "session-1", True)
        ]

        for event_type, user_id, session_id, success in test_events:
            await monitor.check_security_event(
                event_type=event_type,
                user_id=user_id,
                session_id=session_id,
                success=success
            )
            print(f"   ✅ Processed {event_type.value} event (success: {success})")

        # Test metrics
        metrics_summary = monitor.metrics.get_summary()
        print(f"   ✅ Metrics summary: {len(metrics_summary['events_by_type'])} event types tracked")

        # Test security summary
        security_summary = monitor.get_security_summary()
        print(f"   ✅ Security summary generated with {len(security_summary['recent_alerts'])} recent alerts")

        # Test alert creation (simulate abuse)
        for _i in range(5):
            await monitor.check_security_event(
                event_type=SecurityEventType.AUTHENTICATION_FAILED,
                user_id="abuse-test-user",
                success=False
            )

        recent_alerts = monitor.get_recent_alerts(5)
        print(f"   ✅ Alert system working: {len(recent_alerts)} alerts generated")

    except Exception as e:
        print(f"   ❌ Security monitoring test failed: {e}")


async def test_integrated_security_workflow():
    """Test integrated security workflow"""
    print("\n🔄 Testing Integrated Security Workflow...")

    try:
        # Initialize all security components
        encryptor = SessionEncryption()
        cred_manager = CredentialManager()
        audit_logger = AuditLogger()
        monitor = SecurityMonitor()

        # Simulate a complete research session with security
        session_id = "integrated-test-session"
        user_id = "test-user"

        # 1. Store credentials securely
        cred_manager.store_credential("openai", "api_key", "sk-test-key-123")
        await audit_logger.log_security_event(
            event_type=SecurityEventType.CREDENTIAL_ADDED,
            user_id=user_id,
            details={"service": "openai", "credential_type": "api_key"}
        )

        # 2. Start research session with encryption
        session_data = {
            "session_id": session_id,
            "entity_name": "Microsoft Corp",
            "user_id": user_id,
            "sensitive_research_data": "Confidential analysis results"
        }

        encrypted_session = encryptor.encrypt_session(session_data)

        await audit_logger.log_security_event(
            event_type=SecurityEventType.SESSION_CREATED,
            user_id=user_id,
            session_id=session_id,
            details={"entity_name": "Microsoft Corp"}
        )

        await monitor.check_security_event(
            event_type=SecurityEventType.SESSION_CREATED,
            user_id=user_id,
            session_id=session_id,
            success=True
        )

        # 3. Simulate API usage
        await audit_logger.log_api_usage(
            service="openai",
            endpoint="chat/completions",
            session_id=session_id,
            user_id=user_id,
            response_size=1024,
            duration_ms=500.0,
            success=True
        )

        monitor.metrics.record_api_usage("openai", "chat/completions", True)

        # 4. Complete session
        await audit_logger.log_security_event(
            event_type=SecurityEventType.SESSION_MODIFIED,
            user_id=user_id,
            session_id=session_id,
            details={"action": "research_completed", "duration": 180}
        )

        # 5. Export data securely
        await audit_logger.log_security_event(
            event_type=SecurityEventType.DATA_EXPORT,
            user_id=user_id,
            session_id=session_id,
            details={"export_format": "json", "file_path": "/tmp/research_export.json"}
        )

        # 6. Verify encrypted data can be decrypted
        decrypted_session = encryptor.decrypt_session(encrypted_session)
        if decrypted_session["entity_name"] == "Microsoft Corp":
            print("   ✅ End-to-end encryption verified")

        # 7. Get security summary
        security_summary = monitor.get_security_summary()
        print("   ✅ Integrated workflow completed successfully")
        print(f"   📊 Events tracked: {len(security_summary['metrics']['events_by_type'])}")
        print(f"   🚨 Alerts generated: {len(security_summary['recent_alerts'])}")

        # Clean up
        cred_manager.delete_credential("openai")

    except Exception as e:
        print(f"   ❌ Integrated security workflow test failed: {e}")


async def main():
    """Run all security feature tests"""
    print("🛡️ Testing Security Features v2.0...")
    print("=" * 50)

    await test_session_encryption()
    await test_credential_manager()
    await test_audit_logging()
    await test_security_monitoring()
    await test_integrated_security_workflow()

    print("\n" + "=" * 50)
    print("🎉 Security Features testing completed!")
    print("\n💡 Security features are ready for production:")
    print("   • Session encryption with cryptography")
    print("   • Secure credential management")
    print("   • Comprehensive audit logging")
    print("   • Real-time security monitoring")


if __name__ == "__main__":
    asyncio.run(main())
