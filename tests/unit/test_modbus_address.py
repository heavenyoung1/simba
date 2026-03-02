from src.domain.value_objects.modbus_address import RegisterAddress

print(RegisterAddress.from_modbus_string('4x35023'))