from src.modbus_simulator.domain.value_objects.signal_value import ScaleConfig, SignalValue

scale = ScaleConfig(min_value=0.0, max_value=6.0, unit="МПа")

# Чтение AI — середина диапазона
v = SignalValue.from_raw_analog(raw=12000, scale=scale)
assert v.engineering == 3.0
assert v.unit == "МПа"
print(f"raw=12000 → {v.engineering} МПа ✅")

# Запись AO — обратное преобразование
v = SignalValue.from_engineering(value=3.0, scale=scale)
assert v.raw == 12000
print(f"3.0 МПа → raw={v.raw} ✅")

# Дискрет
v = SignalValue.from_discrete(True)
assert v.raw == 1 and v.engineering is True
print("Дискрет True ✅")

print("\n✅ signal_value.py готов")