class BaseCustomException(Exception):
    """Базовый класс для всех исключений в приложении."""

    def __init__(self, message: str = 'Произошла ошибка'):
        self.message = message
        super().__init__(self.message)


class DomainError(Exception):
    """Базовое исключение домена."""

    pass


class SignalNotFoundError(DomainError):
    """Сигнал с указанным тегом не найден в устройстве"""


class SignalNotWritableError(DomainError):
    """Попытка записи в сигнал только для чтения (DI или AI)."""

    def __init__(self, signal_tag: str, signal_type: str):
        super().__init__(f"Сигнал '{signal_tag}' ({signal_type}) — только чтение")
        self.signal_tag = signal_tag
