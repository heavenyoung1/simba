from src.domain.value_objects.enums import XMLHeadObjects, XMLObjects

import xml.etree.ElementTree as ET
from pathlib import Path

class XMLParser:
    def __init__(
            self, 
            file_path: str, 
            xml_objects: XMLHeadObjects,
            xml_iter_objects: XMLObjects,
            ):
        self.file_path = Path(file_path)
        self.xml_objects = xml_objects
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
        for i in self.xml_objects:
            print(i.name, i.value)
            outputs = root.find(i.value)
            print(outputs)
            for iter_obj in outputs:
                print(iter_obj)
                


    

xml_parser = XMLParser(
    file_path='src/infrastructure/test.xml', 
    xml_objects=XMLHeadObjects,
    xml_iter_objects=XMLObjects,
    )
xml_parser.parse()

# xml_parser = XMLParser()
# xml_parser.parse('')

# xml_parser = XMLParser()
# xml_parser.parse('src/infrastructure/test.xml')
