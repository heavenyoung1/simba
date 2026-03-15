from src.domain.entities.analog import AnalogSignal
from src.domain.entities.discrete import DiscreteSignal

from src.application.logger import logger

class RegisterAssembler:
    '''
    Собирает карту регистров Modbus из доменных сигналов.

    Преобразует список AnalogSignal и DiscreteSignal в словарь
    {номер_регистра: значение}, готовый к передаче в ПЛК.

    Дискретные сигналы упаковываются побитово в один регистр.
    Аналоговые сигналы записываются целиком с учётом масштабирования.
    '''

    def build(
        self,
        signals: list[AnalogSignal | DiscreteSignal]
    ) -> dict[int, int]:
        '''Формирует карту регистров из списка сигналов.

        Returns:
            dict[int, int]: {номер_регистра: значение}
        '''
        registers  = {}
        for signal in signals:

            if isinstance(signal, DiscreteSignal):
                self._collect_discrete(signal, registers)
            
            if isinstance(signal, AnalogSignal):
                self._collect_analog(signal, registers)
                
        logger.debug(registers)
        return registers
    

    def _collect_discrete(
            self,
            signal: DiscreteSignal,
            registers: dict[int, int],
            ):
        '''
        Записывает дискретный сигнал в нужный бит регистра.

        Несколько дискретных сигналов могут занимать разные биты
        одного и того же регистра — они аккумулируются через побитовое OR.
        Если сигнал форсирован, используется forced_value, иначе current_value.
        '''
        reg_num = signal.address.address
        if reg_num not in registers:
            registers[reg_num] = 0
        bites = registers[reg_num]  # берём текущее значение регистра
        if signal.forced:
            bites |= (signal.forced_value << signal.address.bit_index)
        else:
            bites |= (signal.current_value << signal.address.bit_index)

        registers[reg_num] = bites  # сохраняем обратно

    def _collect_analog(
            self,
            signal: AnalogSignal,
            registers: dict[int, int],
            ):
        '''
        Записывает аналоговый сигнал в регистр с учётом масштабирования и форсирования.

        Логика выбора значения:
            - forced=False + scaling_enabled  → scale(current_value_eu)
            - forced=False + без скейлинга    → current_value_eu
            - forced=True  + forced_input     → scale(forced_value)
            - forced=True  + not forced_input → forced_value напрямую
        '''
        reg_num = signal.address.address
        if reg_num not in registers:
            registers[reg_num] = 0
        value = registers[reg_num]
        if not signal.forced:
            if signal.scaling_enabled and signal.scaling:
                value = signal.scaling.scale(signal.current_value_eu)
            else:
                value = signal.current_value_eu
        elif signal.forced and signal.forced_input:
            value = signal.scaling.scale(signal.forced_value)
        elif signal.forced and not signal.forced_input:
            value = signal.forced_value
        
        registers[reg_num] = int(value)