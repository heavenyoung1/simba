from src.domain.entities.analog import AnalogSignal
from src.domain.entities.discrete import DiscreteSignal

class RegisterAssembler:
    def build(
        self, 
        signals: list[AnalogSignal | DiscreteSignal]
    ) -> dict[int, int]:
        registers  = {}
        for signal in signals:
            if isinstance(signal, DiscreteSignal):
                reg_num = signal.address.address
                if reg_num not in registers:
                    registers[reg_num] = 0
                bites = registers[reg_num]  # берём текущее значение регистра
                if signal.forced:
                    bites |= (signal.forced_value << signal.address.bit_index)
                    registers[reg_num] = bites
                else:
                    bites |= (signal.current_value << signal.address.bit_index)

                registers[reg_num] = bites  # сохраняем обратно


reg = RegisterAssembler()
reg.build([AnalogSignal, DiscreteSignal])
