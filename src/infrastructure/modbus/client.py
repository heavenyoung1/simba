from pymodbus.client import ModbusTcpClient

class ModbusTCPClient:
    def __init__(
            self,
            host: str, 
            port: int = 502,
            timeout: float = 5.0,
            ):
        self.host = host
        self.port = port
        self.timeout = timeout

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass


