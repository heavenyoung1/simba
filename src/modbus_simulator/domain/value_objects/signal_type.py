from enum import Enum


class SignalType(Enum):
    '''
    Четыре фундаментальных типа сигналов в промышленной автоматизации.

    Определяет таблицу адресного пространства Modbus и правила доступа.
    Прямое соответствие таблицам Modbus:
        DI → Discrete Inputs   (1x) — только чтение,  1 бит
        DO → Coils             (0x) — чтение/запись, 1 бит
        AI → Input Registers   (3x) — только чтение,  16 бит
        AO → Holding Registers (4x) — чтение/запись, 16 бит
    '''
    DI = 'DI'
    DO = 'DO'
    AI = 'AI'
    AO = 'AO'

    def is_writable(self) -> bool:
        '''Возвращает True, если в регистр данного типа разрешена запись (DO, AO).'''
        return self in (SignalType.AO , SignalType.DO)

    def is_analog(self) -> bool:
        '''Возвращает True для аналоговых сигналов (AI, AO), требующих масштабирования.'''
        return self in (SignalType.AI, SignalType.AO)

    def is_discrete(self) -> bool:
        '''Возвращает True для дискретных сигналов (DI, DO), хранящих значение 0 или 1.'''
        return self in (SignalType.DI, SignalType.DO)
    
