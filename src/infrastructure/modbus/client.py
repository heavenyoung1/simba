from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ConnectionException

from src.application.logger import logger


class ModbusClient:
    def __init__(
        self,
        host: str,                          # IP адрес ПЛК
        port: int = 502,                    # TCP-порт Modbus
        timeout: float = 1.0,               # таймаут соединения и запроса
        retries: int = 3,                   # Количество реконнектов
        slave: int = 1,                     # ID устройства на шине Modbus
        reconnect_delay: float = 1.0,       # задержка перед повторным подключением
        reconnect_delay_max: float = 60.0,  # MAX задержка перед повторным подключением
    ):
        self.host=host
        self.port=port
        self.slave = slave
        self._client = AsyncModbusTcpClient(
            host=host,
            port=port,
            timeout=timeout,
            retries=retries,
            reconnect_delay=reconnect_delay,
            reconnect_delay_max=reconnect_delay_max,
        )

    @property
    def connected(self) -> bool:
        return self._client.connected
    
    async def connect(self) -> bool:
        '''Открывает TCP-соединение'''
        if self.connected:
            logger.debug('Соединение уже установлено → %s:%d', self.host, self.port)
            return True
        
        try:
            success = await self._client.connect()
            if success:
                logger.info('Modbus TCP подключение установлено → %s:%d', self.host, self.port)
                return True
            else:
                logger.warning('Не удалось подключиться → %s:%d', self.host, self.port)
                return False
            
        except ConnectionException as e:
            logger.error('Ошибка соединения (ConnectionException) → %s:%d : %s', self.host, self.port, e)
            return False
        except Exception as e:
            logger.error('Неожиданная ошибка при подключении → %s:%d : %s', self.host, self.port, e)
            return False
            
    async def disconnect(self):
        '''Закрывает TCP-соединение'''
        if self._client:
            self._client.close()
            logger.info('Modbus-соединение закрыто → %s:%d', self.host, self.port)

    async def __aenter__(self):
        if not await self.connect():
            raise RuntimeError(f'Не удалось установить соединение в async with → {self.host}:{self.port}')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def ensure_connected(self) -> None:
        '''Гарантирует подключение или кидает исключение'''
        if not await self.connect():
            raise RuntimeError(f'Не удалось подключиться к {self.host}:{self.port}')

    async def read_holding_registers(
        self,
        address: int,
        count: int = 1,
    ):
        try:
            result = await self._client.read_holding_registers(
                address=address,
                count=count,
                device_id=self.slave
            )

            if result.isError():
                raise RuntimeError('Ошибка ModBus протокола ')

            return result.registers
        
        except Exception as e:
            logger.error('Ошибка чтения [addr=%d, count=%d]: %s', address, count, e)
            raise

    
    async def write_registers(self, registers: dict[int, int]) -> None:
        try:
            for addr, value in registers.items():
                result = await self._client.write_register(
                    address=addr,
                    value=value,
                    device_id=self.slave,
                )
                if result.isError():
                    raise RuntimeError('Ошибка ModBus протокола ')
        except Exception as e:
            raise