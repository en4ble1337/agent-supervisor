from unittest.mock import AsyncMock, MagicMock, patch

import asyncssh
import pytest

from backend.services.ssh_service import SSHService


@pytest.mark.asyncio
@patch("backend.services.ssh_service.asyncssh.connect")
async def test_validate_connection_success(mock_connect):
    # Mocking a successful connection as an async context manager
    mock_conn = AsyncMock()
    mock_connect.return_value.__aenter__.return_value = mock_conn
    mock_connect.return_value.__aexit__.return_value = None

    service = SSHService()
    result = await service.validate_connection("10.0.0.5", "admin", "password")

    assert result is True
    mock_conn.run.assert_called_once_with("true", check=True)
    mock_connect.assert_called_once()
    args, kwargs = mock_connect.call_args
    assert args[0] == "10.0.0.5"
    assert kwargs["username"] == "admin"
    assert kwargs["password"] == "password"
    assert "known_hosts" in kwargs
    assert kwargs["connect_timeout"] == 10


@pytest.mark.asyncio
@patch("backend.services.ssh_service.asyncssh.connect")
async def test_validate_connection_returns_false_when_validation_command_fails(mock_connect):
    mock_conn = AsyncMock()
    mock_conn.run.side_effect = OSError("command execution failed")
    mock_connect.return_value.__aenter__.return_value = mock_conn
    mock_connect.return_value.__aexit__.return_value = None

    service = SSHService()
    result = await service.validate_connection("10.0.0.5", "admin", "password")

    assert result is False
    mock_conn.run.assert_called_once_with("true", check=True)


@pytest.mark.asyncio
@patch("backend.services.ssh_service.asyncssh.connect")
async def test_validate_connection_raises_connection_error_when_requested(mock_connect):
    mock_connect.side_effect = OSError("command execution failed")

    service = SSHService()
    with pytest.raises(OSError, match="command execution failed"):
        await service.validate_connection("10.0.0.5", "admin", "password", raise_on_error=True)


@pytest.mark.asyncio
@patch("backend.services.ssh_service.asyncssh.connect")
async def test_validate_connection_timeout(mock_connect):
    # Mocking a timeout error
    mock_connect.side_effect = TimeoutError()

    service = SSHService()
    result = await service.validate_connection("10.0.0.5", "admin", "password")

    assert result is False


@pytest.mark.asyncio
@patch("backend.services.ssh_service.asyncssh.connect")
async def test_validate_connection_auth_failure(mock_connect):
    # Mocking an auth failure
    mock_connect.side_effect = asyncssh.PermissionDenied("Auth failed")

    service = SSHService()
    result = await service.validate_connection("10.0.0.5", "admin", "wrong_password")

    assert result is False


@pytest.mark.asyncio
@patch("backend.services.ssh_service.asyncssh.connect")
async def test_list_directory_success(mock_connect):
    mock_conn = AsyncMock()
    mock_sftp = AsyncMock()
    mock_connect.return_value.__aenter__.return_value = mock_conn

    # Mocking start_sftp_client as a method returning an async context manager
    mock_conn.start_sftp_client = MagicMock()
    mock_sftp_cm = AsyncMock()
    mock_sftp_cm.__aenter__.return_value = mock_sftp
    mock_conn.start_sftp_client.return_value = mock_sftp_cm

    # Mocking SFTP name objects
    mock_file = AsyncMock()
    mock_file.filename = "app.py"
    mock_file.attrs.permissions = 0o100644  # Regular file

    mock_dir = AsyncMock()
    mock_dir.filename = "src"
    mock_dir.attrs.permissions = 0o040755  # Directory

    mock_sftp.readdir.return_value = [mock_file, mock_dir]

    service = SSHService()
    result = await service.list_directory("10.0.0.1", "user", "pass", "/home/user")

    assert len(result) == 2
    assert result[0]["name"] == "app.py"
    assert result[0]["type"] == "file"
    assert result[1]["name"] == "src"
    assert result[1]["type"] == "directory"


@pytest.mark.asyncio
@patch("backend.services.ssh_service.asyncssh.connect")
async def test_read_log_file_success(mock_connect):
    mock_conn = AsyncMock()
    mock_connect.return_value.__aenter__.return_value = mock_conn

    mock_result = AsyncMock()
    mock_result.stdout = "log line 1\nlog line 2"
    mock_result.exit_status = 0
    mock_conn.run.return_value = mock_result

    service = SSHService()
    result = await service.read_log_file("10.0.0.1", "user", "pass", "/var/log/app.log")

    assert result == "log line 1\nlog line 2"
    mock_conn.run.assert_called_once()
    assert "tail -n 100" in mock_conn.run.call_args[0][0]
