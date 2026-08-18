import pytest
from cryptography.fernet import Fernet

from backend.services.crypto_service import CryptoService


def test_crypto_service_encrypt_decrypt():
    key = Fernet.generate_key().decode()
    service = CryptoService(key)

    original_text = "my_secret_ssh_password"
    encrypted_text = service.encrypt(original_text)

    assert encrypted_text != original_text
    assert isinstance(encrypted_text, str)
    assert encrypted_text.startswith("v1:")

    decrypted_text = service.decrypt(encrypted_text)
    assert decrypted_text == original_text


def test_crypto_service_decrypts_legacy_fernet_tokens():
    key = Fernet.generate_key().decode()
    legacy_token = Fernet(key.encode("utf-8")).encrypt(b"legacy_secret").decode("utf-8")
    service = CryptoService(key)

    assert service.decrypt(legacy_token) == "legacy_secret"


def test_crypto_service_invalid_key():
    with pytest.raises(ValueError):
        CryptoService("invalid_length_key")


def test_crypto_service_decrypt_invalid_token():
    key = Fernet.generate_key().decode()
    service = CryptoService(key)

    with pytest.raises(ValueError):
        service.decrypt("invalid_token")
