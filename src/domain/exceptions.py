class BaseCustomException(Exception):
    '''Базовый класс для всех исключений в приложении.'''

    def __init__(self, message: str = 'Произошла ошибка'):
        self.message = message
        super().__init__(self.message)

class ModbusError(Exception):
    '''Базовое исключение клиента'''


class ModbusConnectionError(ModbusError):
    '''Нет соединения с сервером'''


class ModbusTimeoutError(ModbusError):
    '''Сервер не ответил вовремя'''


class ModbusResponseError(ModbusError):
    '''Сервер вернул ошибку или некорректный ответ'''