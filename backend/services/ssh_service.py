import asyncio
import logging
import shlex
import stat
from typing import Any

import asyncssh

logger = logging.getLogger(__name__)
SSH_TIMEOUT_SECONDS = 5
MAX_TEXT_FILE_BYTES = 1_000_000
DEFAULT_WORKSPACE_ROOT = "/opt/hermes/workspace"
DEFAULT_LOG_PATH = "/var/log/syslog"


def _split_host_port(ip_address: str) -> tuple[str, int | None]:
    """Allow dev targets like 127.0.0.1:8022 without adding a schema field yet."""
    if ip_address.count(":") == 1:
        host, port_text = ip_address.rsplit(":", 1)
        if host and port_text.isdigit():
            return host, int(port_text)
    return ip_address, None


def _connection_kwargs(username: str, password: str, port: int | None, timeout: int) -> dict[str, object]:
    kwargs: dict[str, object] = {
        "username": username,
        "password": password,
        "known_hosts": None,
        "connect_timeout": timeout,
    }
    if port is not None:
        kwargs["port"] = port
    return kwargs


class SSHService:
    async def validate_connection(
        self, ip_address: str, username: str, password: str, *, raise_on_error: bool = False
    ) -> bool:
        """Validates SSH connection and authentication."""
        host, port = _split_host_port(ip_address)
        try:
            async with asyncio.timeout(SSH_TIMEOUT_SECONDS):
                async with asyncssh.connect(
                    host,
                    **_connection_kwargs(username, password, port, SSH_TIMEOUT_SECONDS),
                ) as conn:
                    await conn.run("true", check=True, timeout=SSH_TIMEOUT_SECONDS)
            return True
        except (TimeoutError, asyncssh.Error, OSError) as exc:
            logger.error(f"SSH validation failed for {ip_address}: {exc}")
            if raise_on_error:
                raise
            return False

    async def list_directory(self, ip_address: str, username: str, password: str, path: str) -> list[dict[str, str]]:
        """Lists directory contents via SFTP."""
        host, port = _split_host_port(ip_address)
        try:
            async with asyncio.timeout(SSH_TIMEOUT_SECONDS):
                async with asyncssh.connect(
                    host,
                    **_connection_kwargs(username, password, port, SSH_TIMEOUT_SECONDS),
                ) as conn:
                    async with conn.start_sftp_client() as sftp:
                        attrs = await sftp.readdir(path)

                        results = []
                        for attr in attrs:
                            # Skip . and ..
                            if attr.filename in (".", ".."):
                                continue

                            file_type = "unknown"
                            if attr.attrs.permissions is not None:
                                if stat.S_ISDIR(attr.attrs.permissions):
                                    file_type = "directory"
                                elif stat.S_ISREG(attr.attrs.permissions):
                                    file_type = "file"

                            results.append({"name": str(attr.filename), "type": file_type})
                        return results
        except (TimeoutError, asyncssh.Error, OSError) as exc:
            logger.error(f"SFTP readdir failed for {ip_address}:{path}: {exc}")
            raise

    async def read_file(self, ip_address: str, username: str, password: str, path: str) -> str:
        """Reads a UTF-8-ish text file through SFTP."""
        host, port = _split_host_port(ip_address)
        try:
            async with asyncio.timeout(SSH_TIMEOUT_SECONDS):
                async with asyncssh.connect(
                    host,
                    **_connection_kwargs(username, password, port, SSH_TIMEOUT_SECONDS),
                ) as conn:
                    async with conn.start_sftp_client() as sftp:
                        remote_file = await sftp.open(path, "rb")
                        async with remote_file as file_obj:
                            data = await file_obj.read(MAX_TEXT_FILE_BYTES + 1)

            if isinstance(data, str):
                content = data
            else:
                if len(data) > MAX_TEXT_FILE_BYTES:
                    raise ValueError("File is too large to preview")
                content = bytes(data).decode("utf-8", errors="replace")
            return content
        except (TimeoutError, asyncssh.Error, OSError) as exc:
            logger.error(f"SFTP read failed for {ip_address}:{path}: {exc}")
            raise

    async def read_log_file(
        self, ip_address: str, username: str, password: str, log_path: str, *, lines: int = 100
    ) -> str:
        """Returns the last 100 lines of a file via SSH tail."""
        host, port = _split_host_port(ip_address)
        safe_lines = max(1, min(lines, 1000))
        try:
            async with asyncio.timeout(SSH_TIMEOUT_SECONDS):
                async with asyncssh.connect(
                    host,
                    **_connection_kwargs(username, password, port, SSH_TIMEOUT_SECONDS),
                ) as conn:
                    safe_path = shlex.quote(log_path)
                    result = await conn.run(f"tail -n {safe_lines} {safe_path}", check=True, timeout=SSH_TIMEOUT_SECONDS)
                return str(result.stdout)
        except (TimeoutError, asyncssh.Error, OSError) as exc:
            logger.error(f"SSH tail failed for {ip_address}:{log_path}: {exc}")
            raise

    async def run_command(self, ip_address: str, username: str, password: str, command: str) -> str:
        """Runs a bounded read-only diagnostic command over SSH."""
        host, port = _split_host_port(ip_address)
        try:
            async with asyncio.timeout(SSH_TIMEOUT_SECONDS):
                async with asyncssh.connect(
                    host,
                    **_connection_kwargs(username, password, port, SSH_TIMEOUT_SECONDS),
                ) as conn:
                    result = await conn.run(command, check=False, timeout=SSH_TIMEOUT_SECONDS)
                stdout = str(result.stdout or "")
                stderr = str(result.stderr or "")
                return (stdout + stderr).strip()
        except (TimeoutError, asyncssh.Error, OSError) as exc:
            logger.error(f"SSH diagnostic command failed for {ip_address}: {exc}")
            raise

    async def resolve_workspace_root(self, ip_address: str, username: str, password: str) -> str:
        """Finds the best read-only workspace root for known Hermes/OpenClaw layouts."""
        command = (
            "for p in /opt/hermes/workspace \"$HOME/.hermes/workspaces\" \"$HOME/.hermes/workspace\" "
            "\"$HOME/workspace\"; do "
            "[ -d \"$p\" ] && printf '%s\\n' \"$p\" && exit 0; "
            "done"
        )
        output = await self.run_command(ip_address, username, password, command)
        root = _first_absolute_path(output)
        return root or DEFAULT_WORKSPACE_ROOT

    async def resolve_log_path(self, ip_address: str, username: str, password: str) -> str:
        """Finds the best default log file for known Hermes/OpenClaw layouts."""
        command = (
            "for p in \"$HOME/.hermes/logs/gateway.log\" \"$HOME/.hermes/logs/agent.log\" "
            "\"$HOME/.hermes/logs/errors.log\" /var/log/hermes/gateway.log /var/log/hermes/agent.log "
            "/var/log/syslog; do "
            "[ -f \"$p\" ] && printf '%s\\n' \"$p\" && exit 0; "
            "done"
        )
        output = await self.run_command(ip_address, username, password, command)
        log_path = _first_absolute_path(output)
        return log_path or DEFAULT_LOG_PATH

    async def collect_runtime_intel(self, ip_address: str, username: str, password: str) -> dict[str, Any]:
        """Collects read-only runtime intelligence through known agent CLIs."""
        command = (
            "run_hermes() { "
            "if [ -x \"$HOME/.hermes/hermes-agent/venv/bin/python\" ]; then "
            "\"$HOME/.hermes/hermes-agent/venv/bin/python\" -m hermes_cli.main \"$@\"; "
            "elif command -v hermes >/dev/null 2>&1; then hermes \"$@\"; "
            "else printf 'Hermes CLI not found\\n'; return 127; fi; "
            "}; "
            "printf '__HERMES_STATUS__\\n'; "
            "run_hermes status --all 2>&1 | sed -n '1,220p'; "
            "printf '\\n__HERMES_CRONS__\\n'; "
            "run_hermes cron list 2>&1 | sed -n '1,160p'; "
            "printf '\\n__HERMES_SESSIONS__\\n'; "
            "run_hermes sessions list 2>&1 | sed -n '1,160p'; "
            "printf '\\n__RUNTIME_PROCESSES__\\n'; "
            "pgrep -af 'hermes_cli.main|openclaw|hermes' 2>/dev/null | sed -n '1,80p' || true"
        )
        output = await self.run_command(ip_address, username, password, command)
        sections = [
            {
                "id": "hermes-status",
                "title": "Hermes Status",
                "content": _section_text(output, "__HERMES_STATUS__", "__HERMES_CRONS__"),
            },
            {
                "id": "hermes-crons",
                "title": "Cron Jobs",
                "content": _section_text(output, "__HERMES_CRONS__", "__HERMES_SESSIONS__"),
            },
            {
                "id": "hermes-sessions",
                "title": "Sessions",
                "content": _section_text(output, "__HERMES_SESSIONS__", "__RUNTIME_PROCESSES__"),
            },
            {
                "id": "runtime-processes",
                "title": "Runtime Processes",
                "content": _section_text(output, "__RUNTIME_PROCESSES__", None),
            },
        ]
        return {"source": "ssh-cli", "sections": sections}

    async def inspect_runtime(self, ip_address: str, username: str, password: str) -> dict[str, Any]:
        """Collects lightweight runtime diagnostics when the native API is unavailable."""
        command = (
            "printf '__PROCESSES__\\n'; "
            "pgrep -af 'hermes_cli.main|openclaw|hermes' 2>/dev/null || true; "
            "printf '\\n__LISTENERS__\\n'; "
            "ss -ltnp 2>/dev/null || ss -ltn 2>/dev/null || true; "
            "printf '\\n__ENV_HINTS__\\n'; "
            "env | grep -E '^(API_SERVER|WEBHOOK|HERMES|OPENCLAW)_' 2>/dev/null || true"
        )
        output = await self.run_command(ip_address, username, password, command)
        processes = _section_lines(output, "__PROCESSES__", "__LISTENERS__")
        listeners = _section_lines(output, "__LISTENERS__", "__ENV_HINTS__")
        env_hints = _section_lines(output, "__ENV_HINTS__", None)
        has_gateway = any("hermes" in line.lower() for line in processes)
        has_api_listener = any(":8642" in line or ":9119" in line or ":18789" in line for line in listeners)

        if has_gateway and not has_api_listener:
            summary = "Hermes/OpenClaw-like process found over SSH, but no expected native API listener is exposed."
        elif has_api_listener:
            summary = "Native API listener appears to exist, but the supervisor API call failed."
        else:
            summary = "SSH is reachable, but no known Hermes/OpenClaw runtime process was found."

        return {
            "summary": summary,
            "processes": processes[:10],
            "listeners": listeners[:20],
            "env_hints": env_hints[:10],
            "api_hint": (
                "For Hermes, enable the api_server adapter on 127.0.0.1:8642 for SSH tunneling "
                "or on 0.0.0.0:8642 with API_SERVER_KEY for direct LAN access."
            ),
        }


def _section_lines(output: str, start_marker: str, end_marker: str | None) -> list[str]:
    if start_marker not in output:
        return []
    section = output.split(start_marker, 1)[1]
    if end_marker and end_marker in section:
        section = section.split(end_marker, 1)[0]
    return [line.strip() for line in section.splitlines() if line.strip()]


def _section_text(output: str, start_marker: str, end_marker: str | None) -> str:
    if start_marker not in output:
        return "No data returned."
    section = output.split(start_marker, 1)[1]
    if end_marker and end_marker in section:
        section = section.split(end_marker, 1)[0]
    text = section.strip()
    return text or "No data returned."


def _first_absolute_path(output: str) -> str | None:
    for line in output.splitlines():
        candidate = line.strip().rstrip("/")
        if candidate.startswith("/"):
            return candidate or "/"
    return None
