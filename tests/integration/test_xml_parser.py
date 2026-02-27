from src.infrastructure.xml_parser import XMLParser
from src.application.register_assembler import RegisterAssembler

from src.domain.value_objects.enums import (
    XMLHeadObjects,
    XMLObjects,
)

xml_parser = XMLParser(
    file_path='src/infrastructure/test.xml',
    xml_head_objects=XMLHeadObjects,
    xml_iter_objects=XMLObjects,
)
register_assembler = RegisterAssembler()

result = xml_parser.parse()
all_signals = result['AnalogOutputs'] + result['DiscreteInputs']

register_assembler.build(all_signals)