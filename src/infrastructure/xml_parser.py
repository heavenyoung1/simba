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

import xml.etree.ElementTree as ET
from pathlib import Path

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
        for i in self.xml_head_objects:
            #print(i.name, i.value)
            elenment_outputs_obj = root.find(i.value)
            elenment_outputs = elenment_outputs_obj.tag
            print(elenment_outputs)
            if elenment_outputs == XMLHeadObjects.ANALOGS.value:
                for iter_obj in elenment_outputs_obj:

                    # Если значение не совпадает ни с одним — Python сам бросит ValueError
                    direction = Direction(iter_obj.find('Direction').text)

                    tag = iter_obj.find('Name').text
                    name = iter_obj.find('Description').text

                    # 2. Нужно сравнить что значение datatype совпадает со значениями в 
                    
                    address = iter_obj.find('Address')
                    driver = address.find('Driver')
                    driver_name = Driver(driver.find('Name').text)
                    driver_type = driver.find('Type').text
                    raw_address = address.find('Address').text
                    number_addrees = int(raw_address[2:])

                    data_type = DataType(address.find('DataType').text)

                    mb_address = RegisterAddress(
                        address=number_addrees,
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

                    signal = AnalogSignal(
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
                    print(signal)



                    
                    


            elif elenment_outputs == XMLHeadObjects.DISCRETES.value:
                for iter_obj in elenment_outputs:
                    pass
                


    

xml_parser = XMLParser(
    file_path='src/infrastructure/test.xml', 
    xml_head_objects=XMLHeadObjects,
    xml_iter_objects=XMLObjects,
    )
xml_parser.parse()

# xml_parser = XMLParser()
# xml_parser.parse('')

# xml_parser = XMLParser()
# xml_parser.parse('src/infrastructure/test.xml')
