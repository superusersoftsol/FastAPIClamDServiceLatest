import socket
from app.logger import get_logger

logger = get_logger(__name__)

class ClamAVService:
    def __init__(self, host="127.0.0.1", port=3310):
        self.host = host
        self.port = port

    def _send_command(self, command: str, data_path: str = None):
        try:
            with socket.create_connection((self.host, self.port), timeout=10) as sock:
                if data_path:
                    sock.sendall(f"{command} {data_path}\n".encode())
                else:
                    sock.sendall(f"{command}\n".encode())
                response = sock.recv(4096).decode().strip()
                return response
        except Exception as e:
            logger.error(f"Error communicating with clamd: {e}")
            raise

    def scan_file(self, file_path: str):
        logger.info(f"Starting ClamAV scan for {file_path}")
        result = self._send_command("SCAN", file_path)
        logger.info(f"Scan completed for {file_path}: {result}")
        return {"result": result}

    def health_check(self):
        try:
            response = self._send_command("PING")
            if response == "PONG":
                logger.info("ClamAV daemon health check passed.")
                return True
            logger.warning(f"Unexpected ClamAV PING response: {response}")
            return False
        except Exception as e:
            logger.error(f"ClamAV daemon health check failed: {e}")
            return False
