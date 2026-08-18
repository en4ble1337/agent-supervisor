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
    mock_conn.run.assert_called_once_with("true", check=True, timeout=5)
    mock_connect.assert_called_once()
    args, kwargs = mock_connect.call_args
    assert args[0] == "10.0.0.5"
    assert kwargs["username"] == "admin"
    assert kwargs["password"] == "password"
    assert "known_hosts" in kwargs
    assert kwargs["connect_timeout"] == 5


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
    mock_conn.run.assert_called_once_with("true", check=True, timeout=5)


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
    args, kwargs = mock_connect.call_args
    assert args[0] == "10.0.0.1"
    assert kwargs["connect_timeout"] == 5


@pytest.mark.asyncio
@patch("backend.services.ssh_service.asyncssh.connect")
async def test_list_directory_supports_host_port_targets(mock_connect):
    mock_conn = AsyncMock()
    mock_sftp = AsyncMock()
    mock_connect.return_value.__aenter__.return_value = mock_conn

    mock_conn.start_sftp_client = MagicMock()
    mock_sftp_cm = AsyncMock()
    mock_sftp_cm.__aenter__.return_value = mock_sftp
    mock_conn.start_sftp_client.return_value = mock_sftp_cm
    mock_sftp.readdir.return_value = []

    service = SSHService()
    result = await service.list_directory("127.0.0.1:8022", "user", "pass", "/opt/hermes/workspace")

    assert result == []
    args, kwargs = mock_connect.call_args
    assert args[0] == "127.0.0.1"
    assert kwargs["port"] == 8022
    assert kwargs["connect_timeout"] == 5


@pytest.mark.asyncio
@patch("backend.services.ssh_service.asyncssh.connect")
async def test_read_file_success(mock_connect):
    mock_conn = AsyncMock()
    mock_sftp = AsyncMock()
    mock_connect.return_value.__aenter__.return_value = mock_conn

    mock_conn.start_sftp_client = MagicMock()
    mock_sftp_cm = AsyncMock()
    mock_sftp_cm.__aenter__.return_value = mock_sftp
    mock_conn.start_sftp_client.return_value = mock_sftp_cm

    mock_remote_file = AsyncMock()
    mock_remote_file.read.return_value = b"# Report\nhello"
    mock_file_cm = AsyncMock()
    mock_file_cm.__aenter__.return_value = mock_remote_file
    mock_sftp.open.return_value = mock_file_cm

    service = SSHService()
    result = await service.read_file("10.0.0.1", "user", "pass", "/opt/hermes/workspace/report.md")

    assert result == "# Report\nhello"
    mock_sftp.open.assert_awaited_once_with("/opt/hermes/workspace/report.md", "rb")
    mock_remote_file.read.assert_awaited_once()
    args, kwargs = mock_connect.call_args
    assert args[0] == "10.0.0.1"
    assert kwargs["connect_timeout"] == 5


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
    mock_conn.run.assert_called_once_with("tail -n 100 /var/log/app.log", check=True, timeout=5)
    args, kwargs = mock_connect.call_args
    assert args[0] == "10.0.0.1"
    assert kwargs["connect_timeout"] == 5


@pytest.mark.asyncio
async def test_resolve_workspace_root_prefers_discovered_hermes_workspaces():
    service = SSHService()
    assert hasattr(service, "resolve_workspace_root")
    service.run_command = AsyncMock(return_value="/home/transcribo/.hermes/workspaces\n")  # type: ignore[method-assign]

    result = await service.resolve_workspace_root("10.0.0.1", "user", "pass")

    assert result == "/home/transcribo/.hermes/workspaces"
    service.run_command.assert_awaited_once()


@pytest.mark.asyncio
async def test_resolve_workspace_root_falls_back_to_arch_default():
    service = SSHService()
    assert hasattr(service, "resolve_workspace_root")
    service.run_command = AsyncMock(return_value="")  # type: ignore[method-assign]

    result = await service.resolve_workspace_root("10.0.0.1", "user", "pass")

    assert result == "/opt/hermes/workspace"


@pytest.mark.asyncio
async def test_resolve_log_path_prefers_discovered_hermes_gateway_log():
    service = SSHService()
    assert hasattr(service, "resolve_log_path")
    service.run_command = AsyncMock(return_value="/home/transcribo/.hermes/logs/gateway.log\n")  # type: ignore[method-assign]

    result = await service.resolve_log_path("10.0.0.1", "user", "pass")

    assert result == "/home/transcribo/.hermes/logs/gateway.log"
    service.run_command.assert_awaited_once()


@pytest.mark.asyncio
async def test_resolve_log_path_falls_back_to_syslog():
    service = SSHService()
    assert hasattr(service, "resolve_log_path")
    service.run_command = AsyncMock(return_value="")  # type: ignore[method-assign]

    result = await service.resolve_log_path("10.0.0.1", "user", "pass")

    assert result == "/var/log/syslog"


@pytest.mark.asyncio
async def test_collect_runtime_intel_parses_read_only_cli_sections():
    service = SSHService()
    service.run_command = AsyncMock(
        return_value=(
            "__HERMES_STATUS__\n"
            "Gateway Service: running\n"
            "Sessions: Active: 1 session(s)\n"
            "\n__HERMES_CRONS__\n"
            "No scheduled jobs.\n"
            "\n__HERMES_SESSIONS__\n"
            "Title  Last Active  ID\n"
            "Research  2h ago  20260503_abc\n"
            "\n__RUNTIME_PROCESSES__\n"
            "123 python -m hermes_cli.main gateway run --replace\n"
        )
    )  # type: ignore[method-assign]

    result = await service.collect_runtime_intel("10.0.0.1", "user", "pass")

    assert result["source"] == "ssh-cli"
    assert result["sections"][0]["id"] == "hermes-status"
    assert "Gateway Service: running" in result["sections"][0]["content"]
    assert result["sections"][1]["id"] == "hermes-crons"
    assert "No scheduled jobs" in result["sections"][1]["content"]
    assert result["sections"][2]["id"] == "hermes-sessions"
    assert "Research" in result["sections"][2]["content"]
    assert result["sections"][3]["id"] == "runtime-processes"
    service.run_command.assert_awaited_once()
