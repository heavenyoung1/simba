from dataclasses import dataclass


@dataclass
class ConnectionConfig:
    host: str = "192.168.1.1"
    port: int = 502
    timeout: float = 3.0
    unit_id: int = 1