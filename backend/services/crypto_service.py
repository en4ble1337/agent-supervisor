from cryptography.fernet import Fernet, InvalidToken


class CryptoService:
    def __init__(self, key: str):
        try:
            # Fernet requires a base64 encoded 32-byte key
            # If the key is not valid base64 or not the right length, this will raise
            self.fernet = Fernet(key.encode("utf-8"))
        except (ValueError, TypeError) as e:
            raise ValueError("Invalid ENCRYPTION_KEY format. Must be a base64-encoded 32-byte key.") from e

    def encrypt(self, data: str) -> str:
        """Encrypts a string and returns a base64 encoded string."""
        return self.fernet.encrypt(data.encode("utf-8")).decode("utf-8")

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypts a base64 encoded string."""
        try:
            return self.fernet.decrypt(encrypted_data.encode("utf-8")).decode("utf-8")
        except InvalidToken as e:
            raise ValueError("Invalid token or key for decryption.") from e
