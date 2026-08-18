import base64
import binascii
import os

from cryptography.exceptions import InvalidTag
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

TOKEN_PREFIX = "v1:"
AESGCM_NONCE_BYTES = 12
ASSOCIATED_DATA = b"agent-supervisor:ssh-password:v1"


class CryptoService:
    def __init__(self, key: str):
        try:
            raw_key = base64.urlsafe_b64decode(key.encode("utf-8"))
            self.aesgcm = AESGCM(raw_key)
            self.fernet = Fernet(key.encode("utf-8"))
        except (binascii.Error, ValueError, TypeError) as e:
            raise ValueError("Invalid ENCRYPTION_KEY format. Must be a base64-encoded 32-byte key.") from e

    def encrypt(self, data: str) -> str:
        """Encrypts a string with AES-256-GCM and returns a versioned token."""
        nonce = os.urandom(AESGCM_NONCE_BYTES)
        ciphertext = self.aesgcm.encrypt(nonce, data.encode("utf-8"), ASSOCIATED_DATA)
        token = base64.urlsafe_b64encode(nonce + ciphertext).decode("utf-8")
        return f"{TOKEN_PREFIX}{token}"

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypts a versioned AES-GCM token, with legacy Fernet read support."""
        if encrypted_data.startswith(TOKEN_PREFIX):
            try:
                payload = base64.urlsafe_b64decode(encrypted_data.removeprefix(TOKEN_PREFIX).encode("utf-8"))
                nonce = payload[:AESGCM_NONCE_BYTES]
                ciphertext = payload[AESGCM_NONCE_BYTES:]
                return self.aesgcm.decrypt(nonce, ciphertext, ASSOCIATED_DATA).decode("utf-8")
            except (binascii.Error, InvalidTag, ValueError) as e:
                raise ValueError("Invalid token or key for decryption.") from e

        try:
            return self.fernet.decrypt(encrypted_data.encode("utf-8")).decode("utf-8")
        except InvalidToken as e:
            raise ValueError("Invalid token or key for decryption.") from e
