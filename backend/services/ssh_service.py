import logging
import shlex
import stat

import asyncssh

logger = logging.getLogger(__name__)


class SSHService:
    async def validate_connection(self, ip_address: str, username: str, password: str) -> bool:
        """Validates SSH connection and authentication."""
        try:
            async with asyncssh.connect(
                ip_address,
                username=username,
                password=password,
                known_hosts=None,
            ):
                pass
            return True
        except (TimeoutError, asyncssh.Error, OSError) as exc:
            logger.error(f"SSH validation failed for {ip_address}: {exc}")
            return False

    async def list_directory(self, ip_address: str, username: str, password: str, path: str) -> list[dict[str, str]]:
        """Lists directory contents via SFTP."""
        try:
            async with asyncssh.connect(
                ip_address,
                username=username,
                password=password,
                known_hosts=None,
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

    async def read_log_file(self, ip_address: str, username: str, password: str, log_path: str) -> str:
        """Returns the last 100 lines of a file via SSH tail."""
        try:
            async with asyncssh.connect(
                ip_address,
                username=username,
                password=password,
                known_hosts=None,
            ) as conn:
                # Use shlex.quote to prevent command injection
                safe_path = shlex.quote(log_path)
                result = await conn.run(f"tail -n 100 {safe_path}", check=True)
                return str(result.stdout)
        except (TimeoutError, asyncssh.Error, OSError) as exc:
            logger.error(f"SSH tail failed for {ip_address}:{log_path}: {exc}")
            raise
