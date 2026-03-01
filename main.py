import asyncio
from src.infrastructure.modbus.server import ModbusServer
from src.infrastructure.xml_parser import XMLParser
from src.domain.value_objects.enums import XMLHeadObjects, XMLObjects

parser = XMLParser('src/infrastructure/test.xml', XMLHeadObjects, XMLObjects)
result = parser.parse()
signals = result['AnalogOutputs'] + result['DiscreteInputs']

server = ModbusServer()
asyncio.run(server.start(signals))