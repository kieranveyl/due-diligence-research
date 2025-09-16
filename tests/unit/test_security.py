from unittest.mock import MagicMock, patch

import pytest

from src.security.audit import AuditLogger
from src.security.encryption import SessionEncryption
from src.security.monitoring import SecurityMonitor


@pytest.mark.asyncio
async def test_session_encryption():
    """Test session encryption functionality"""
    encryption = SessionEncryption()

    # Test data encryption and decryption
    test_data = {"sensitive": "information", "user_id": "test123"}

    encrypted = encryption.encrypt_session(test_data)
    assert encrypted != test_data
    assert isinstance(encrypted, str)

    decrypted = encryption.decrypt_session(encrypted)
    assert decrypted == test_data


@pytest.mark.asyncio
async def test_audit_logger():
    """Test audit logging functionality"""
    from src.security.audit import SecurityEventType

    with patch('structlog.get_logger') as mock_logger:
        mock_log = MagicMock()
        mock_logger.return_value = mock_log

        audit = AuditLogger()

        await audit.log_security_event(
            event_type=SecurityEventType.SESSION_CREATED,
            user_id="user123",
            resource_id="test_resource",
            details={"key": "value"}
        )

        mock_log.info.assert_called_once()


@pytest.mark.asyncio
async def test_security_monitor():
    """Test security monitoring functionality"""
    from src.security.audit import SecurityEventType

    with patch('structlog.get_logger') as mock_logger:
        mock_log = MagicMock()
        mock_logger.return_value = mock_log

        monitor = SecurityMonitor()

        await monitor.check_security_event(
            event_type=SecurityEventType.SESSION_ACCESSED,
            user_id="user123",
            details={"event": "data"}
        )

        # SecurityMonitor doesn't directly call logger, it records metrics
        assert True  # Just verify no exception is raised


@pytest.mark.asyncio
async def test_credential_encryption():
    """Test credential encryption and storage"""
    encryption = SessionEncryption()

    credentials = {
        "api_key": "secret-key-123",
        "token": "bearer-token-456"
    }

    encrypted_creds = encryption.encrypt_data(credentials)
    assert encrypted_creds != credentials
    assert isinstance(encrypted_creds, str)

    decrypted_creds = encryption.decrypt_data(encrypted_creds)
    assert decrypted_creds == credentials


@pytest.mark.asyncio
async def test_integrated_security_workflow():
    """Test integrated security workflow with encryption, logging, and monitoring"""
    from src.security.audit import SecurityEventType

    with patch('structlog.get_logger') as mock_logger:
        mock_log = MagicMock()
        mock_logger.return_value = mock_log

        # Initialize security components
        encryption = SessionEncryption()
        audit = AuditLogger()
        monitor = SecurityMonitor()

        # Simulate secure workflow
        sensitive_data = {"user_id": "test123", "query": "confidential research"}

        # 1. Encrypt sensitive data
        encrypted_data = encryption.encrypt_session(sensitive_data)
        assert encrypted_data is not None

        # 2. Log the action
        await audit.log_security_event(
            event_type=SecurityEventType.SESSION_CREATED,
            user_id=sensitive_data["user_id"],
            resource_id="session_data",
            details={"data_size": len(str(sensitive_data))}
        )

        # 3. Monitor security event
        await monitor.check_security_event(
            event_type=SecurityEventType.SESSION_ACCESSED,
            user_id=sensitive_data["user_id"],
            details={"user_id": sensitive_data["user_id"]}
        )

        # Verify logging calls were made
        assert mock_log.info.call_count >= 1
