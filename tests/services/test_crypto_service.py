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

    decrypted_text = service.decrypt(encrypted_text)
    assert decrypted_text == original_text


def test_crypto_service_invalid_key():
    with pytest.raises(ValueError):
        CryptoService("invalid_length_key")


def test_crypto_service_decrypt_invalid_token():
    key = Fernet.generate_key().decode()
    service = CryptoService(key)

    with pytest.raises(ValueError):
        service.decrypt("invalid_token")
