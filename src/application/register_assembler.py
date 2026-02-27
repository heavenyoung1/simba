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
            
            if isinstance(signal, AnalogSignal):
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
                
        return registers


reg = RegisterAssembler()
reg.build([AnalogSignal, DiscreteSignal])
