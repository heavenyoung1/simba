from src.domain.value_objects.enums import XMLHeadObjects, XMLObjects
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

    # def parse(self, file_path: str):
    #     self.file_path = Path(file_path)
    #     tree = ET.parse(self.file_path)
    #     root = tree.getroot()
    #     print(root)
    #     #analog = root.find(XMLObjects.ANALOGS)
    #     analog = root.find('AnalogOutputs')
    #     print(analog)
    #     aus = analog.find('Analog')
    #     print(aus.find('Direction').text)   # → 'WRITING'
    #     print(aus.find('Name').text)        # → 'KKC004'

    # def parse(self, file_path: str):
    #     self.file_path = Path(file_path)
    #     tree = ET.parse(self.file_path)
    #     root = tree.getroot()
    #     print(root)
    #     # analog_outputs = root.find('AnalogOutputs')
    #     # analogs = analog_outputs.findall('Analog')
        
    #     analog_outputs = root.find(XMLObjects.ANALOGS.value)
    #     namesss = XMLObjects.ANALOGS.name
    #     print(namesss)
    #     analogs = analog_outputs.findall('Analog')
        
    #     print(analogs)

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
                    direction = iter_obj.find('Direction').text
                    tag = iter_obj.find('Name').text
                    name = iter_obj.find('Description').text
                    
                    address = iter_obj.find('Address')
                    driver = address.find('Driver')
                    driver_name = driver.find('Name').text
                    driver_type = driver.find('Type').text
                    data_type = address.find('DataType').text


                    forced = iter_obj.find('Forced').text
                    forced_value = iter_obj.find('ForcedValue').text
                    forced_input = iter_obj.find('ForceInput').text

                    scaling_enabled = iter_obj.find('Scaling').text.lower() == 'true'
                    scaling = None

                    if scaling_enabled:
                        min_input = float(iter_obj.find('MinInput').text)
                        max_input = float(iter_obj.find('MaxInput').text)
                        min_output = float(iter_obj.find('MinOutput').text)
                        max_output = float(iter_obj.find('MaxOutput').text)
                    
                    return AnalogSignal(
                        direction=direction,
                        tag=tag,
                        name=name,
                        address=address,
                        data_type=data_type,
                        
                        driver=driver,
                        scaling=scaling,
                        scaling_enabled=scaling_enabled,
                        forced=forced,
                        forced_input=forced_input,
                        forced_value=forced_value,

    )

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
