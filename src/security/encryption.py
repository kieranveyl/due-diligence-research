"""
Session Encryption and Credential Management
"""

import base64
import json
import os
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.config.settings import settings


class SessionEncryption:
    """Handles encryption/decryption of sensitive session data"""

    def __init__(self):
        self.encryption_key = self._get_or_create_encryption_key()
        self.fernet = Fernet(self.encryption_key)

    def _get_or_create_encryption_key(self) -> bytes:
        """Get encryption key from environment or generate new one"""
        if hasattr(settings, 'session_encryption_key') and settings.session_encryption_key:
            # Use provided key from settings
            key_str = str(settings.session_encryption_key)
            if key_str.startswith('secret:'):
                key_str = key_str[7:]  # Remove 'secret:' prefix

            try:
                # Try to use as base64 encoded key
                return base64.urlsafe_b64decode(key_str.encode())
            except Exception:
                # Derive key from provided string
                return self._derive_key_from_password(key_str)
        else:
            # Generate new key and save to config
            key = Fernet.generate_key()
            self._save_encryption_key(key)
            return key

    def _derive_key_from_password(self, password: str) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        salt = b'due_diligence_salt_v1'  # Fixed salt for consistency
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def _save_encryption_key(self, key: bytes):
        """Save encryption key to secure location"""
        config_dir = Path.home() / ".config" / "due-diligence"
        config_dir.mkdir(parents=True, exist_ok=True)

        key_file = config_dir / "encryption.key"
        with open(key_file, "wb") as f:
            f.write(key)

        # Set restrictive permissions
        os.chmod(key_file, 0o600)

        print(f"🔐 Generated new encryption key saved to: {key_file}")
        print("⚠️  Keep this key secure - needed to decrypt existing sessions")

    def encrypt_data(self, data: Any) -> str:
        """Encrypt arbitrary data to base64 string"""
        json_data = json.dumps(data, default=str)
        encrypted_bytes = self.fernet.encrypt(json_data.encode())
        return base64.urlsafe_b64encode(encrypted_bytes).decode()

    def decrypt_data(self, encrypted_data: str) -> Any:
        """Decrypt base64 string back to original data"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_bytes = self.fernet.decrypt(encrypted_bytes)
            return json.loads(decrypted_bytes.decode())
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {e}")

    def encrypt_session(self, session_data: dict[str, Any]) -> str:
        """Encrypt session data for secure storage"""
        return self.encrypt_data(session_data)

    def decrypt_session(self, encrypted_session: str) -> dict[str, Any]:
        """Decrypt session data from secure storage"""
        return self.decrypt_data(encrypted_session)


class CredentialManager:
    """Secure credential management for API keys and sensitive data"""

    def __init__(self):
        self.encryptor = SessionEncryption()
        self.credentials_file = Path.home() / ".config" / "due-diligence" / "credentials.enc"
        self.credentials_file.parent.mkdir(parents=True, exist_ok=True)

    def store_credential(self, service: str, credential_type: str, value: str):
        """Store encrypted credential"""
        credentials = self._load_credentials()

        if service not in credentials:
            credentials[service] = {}

        credentials[service][credential_type] = value
        self._save_credentials(credentials)

    def get_credential(self, service: str, credential_type: str) -> str | None:
        """Retrieve decrypted credential"""
        credentials = self._load_credentials()
        return credentials.get(service, {}).get(credential_type)

    def delete_credential(self, service: str, credential_type: str = None):
        """Delete credential(s)"""
        credentials = self._load_credentials()

        if service in credentials:
            if credential_type:
                credentials[service].pop(credential_type, None)
                if not credentials[service]:  # Remove empty service
                    del credentials[service]
            else:
                del credentials[service]

        self._save_credentials(credentials)

    def list_services(self) -> dict[str, list]:
        """List all services and their credential types"""
        credentials = self._load_credentials()
        return {
            service: list(creds.keys())
            for service, creds in credentials.items()
        }

    def _load_credentials(self) -> dict[str, dict[str, str]]:
        """Load and decrypt credentials from file"""
        if not self.credentials_file.exists():
            return {}

        try:
            with open(self.credentials_file) as f:
                encrypted_data = f.read()

            if not encrypted_data.strip():
                return {}

            return self.encryptor.decrypt_data(encrypted_data)
        except Exception as e:
            print(f"⚠️ Failed to load credentials: {e}")
            return {}

    def _save_credentials(self, credentials: dict[str, dict[str, str]]):
        """Encrypt and save credentials to file"""
        try:
            encrypted_data = self.encryptor.encrypt_data(credentials)

            with open(self.credentials_file, "w") as f:
                f.write(encrypted_data)

            # Set restrictive permissions
            os.chmod(self.credentials_file, 0o600)

        except Exception as e:
            print(f"❌ Failed to save credentials: {e}")
            raise

    def rotate_encryption_key(self):
        """Rotate encryption key and re-encrypt all credentials"""
        # Load current credentials
        old_credentials = self._load_credentials()

        # Generate new encryption key
        new_key = Fernet.generate_key()
        self.encryptor.encryption_key = new_key
        self.encryptor.fernet = Fernet(new_key)

        # Re-encrypt with new key
        self._save_credentials(old_credentials)

        # Save new encryption key
        self.encryptor._save_encryption_key(new_key)

        print("🔄 Encryption key rotated successfully")

    def validate_credentials(self) -> dict[str, bool]:
        """Validate stored credentials against current settings"""
        validation_results = {}

        # Check required credentials
        required_credentials = {
            "openai": "api_key",
            "exa": "api_key",
            "tavily": "api_key"
        }

        for service, cred_type in required_credentials.items():
            stored_value = self.get_credential(service, cred_type)
            env_value = getattr(settings, f"{service}_api_key", None)

            # Credential is valid if either stored or in environment
            validation_results[service] = bool(stored_value or env_value)

        return validation_results
