import xml.etree.ElementTree as ET
from pathlib import Path

from src.domain.value_objects.enums import (
    XMLHeadObjects,
    XMLObjects,
    DataType,
    Direction,
    Driver,
)
from src.domain.value_objects.modbus_address import RegisterAddress
from src.domain.value_objects.scaling import ScalingRule

from src.domain.entities.analog import AnalogSignal
from src.domain.entities.discrete import DiscreteSignal


class XMLParser:
    def __init__(
            self,
            file_path: str,
            xml_head_objects: XMLHeadObjects,
            xml_iter_objects: XMLObjects,
    ):
        self.file_path = Path(file_path)
        self.xml_head_objects = xml_head_objects
        self.xml_iter_objects = xml_iter_objects

    def parse(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        output = {}

        for i in self.xml_head_objects:
            element_obj = root.find(i.value)
            element_tag = element_obj.tag
            output[element_tag] = []

            if element_tag == XMLHeadObjects.ANALOGS.value:
                for iter_obj in element_obj:
                    signal = self._parse_analog(iter_obj)
                    output[element_tag].append(signal)

            elif element_tag == XMLHeadObjects.DISCRETES.value:
                for iter_obj in element_obj:
                    signal = self._parse_discret(iter_obj)
                    output[element_tag].append(signal)

        print(output)
        return output

    def _parse_analog(self, iter_obj) -> AnalogSignal:
        direction = Direction(iter_obj.find('Direction').text)
        tag = iter_obj.find('Name').text
        name = iter_obj.find('Description').text

        address = iter_obj.find('Address')
        driver = address.find('Driver')
        driver_name = Driver(driver.find('Name').text)
        # TODO Возможно этот атрибут пригодится, когда будет парсинг не только MB
        driver_type = driver.find('Type').text
        raw_address = address.find('Address').text
        number_address = int(raw_address[2:])
        data_type = DataType(address.find('DataType').text)

        mb_address = RegisterAddress(
            address=number_address,
            bit_index=None,
        )

        min_input = float(iter_obj.find('MinInput').text)
        max_input = float(iter_obj.find('MaxInput').text)
        min_output = float(iter_obj.find('MinOutput').text)
        max_output = float(iter_obj.find('MaxOutput').text)

        scaling_enabled = iter_obj.find('Scaling').text.lower() == 'true'

        scaling = ScalingRule(
            min_eu=min_input,
            max_eu=max_input,
            min_raw=min_output,
            max_raw=max_output,
        )

        forced = iter_obj.find('Forced').text.lower() == 'true'
        forced_value = float(iter_obj.find('ForcedValue').text)
        forced_input = iter_obj.find('ForceInput').text.lower() == 'true'

        return AnalogSignal(
            direction=direction,
            tag=tag,
            name=name,
            data_type=data_type,
            address=mb_address,
            driver=driver_name,
            scaling=scaling if scaling_enabled else None,
            scaling_enabled=scaling_enabled,
            forced=forced,
            forced_input=forced_input,
            forced_value=forced_value,
        )
    
    def _parse_discret(self, iter_obj) -> DiscreteSignal:
        direction = Direction(iter_obj.find('Direction').text)
        tag = iter_obj.find('Name').text
        name = iter_obj.find('Description').text

        address = iter_obj.find('Address')
        driver = address.find('Driver')
        driver_name = Driver(driver.find('Name').text)
        # TODO Возможно этот атрибут пригодится, когда будет парсинг не только MB
        driver_type = driver.find('Type').text
        raw_address = address.find('Address').text
        number_address = int(raw_address[2:])
        # Если это Дискрет, то тут же всегда BOOLEAN #TODO ПОДУМАТЬ
        data_type = DataType(address.find('DataType').text)
        # TODO Нужна ли тут валидация, если биты могут быть 0-15 ПОДУМАТЬ
        bit_index = int(address.find('BitIndex').text)

        mb_address = RegisterAddress(
            address=number_address,
            bit_index=bit_index,
        )

        forced = iter_obj.find('Forced').text.lower() == 'true'
        forced_value = bool(iter_obj.find('ForcedValue').text)
        inversed = iter_obj.find('Inversed').text

        return DiscreteSignal(
            direction=direction,
            tag=tag,
            name=name,
            address=mb_address,
            inversed=inversed,
            driver=driver,
            forced=forced,
            forced_value=forced_value,
        )

xml_parser = XMLParser(
    file_path='src/infrastructure/test.xml',
    xml_head_objects=XMLHeadObjects,
    xml_iter_objects=XMLObjects,
)
xml_parser.parse()
