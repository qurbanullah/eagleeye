import xml.etree.ElementTree as ET

class Parse:

    def __init__(self):
        self
        # self.xml_node = xml_node
        # self.xml_file = xml_file

      
    def get_xml_element_text_from_package_file(self, xml_node, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for package in root.findall('.'):
            node_name = package.find(xml_node).text            
            return node_name


    def get_xml_date_element_text_from_package_database_file(self, xml_file, xml_node):
        # def get_xml_node_from_file(self, xml_file, xml_root):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        node = "./"+"".join(xml_node) +""
        # print(node)
        data = root.find(node)
        return (data.text)



    def get_xml_element_text_from_package_database_file(self, xml_file, xml_root, xml_node):
        # def get_xml_node_from_file(self, xml_file, xml_root):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        node = "./"+"".join(xml_root) +"/Package/"+"".join(xml_node) +""
        # node = "./"+"".join(xml_root) +"/Package/"+""
        for child in root.findall(node) :
            # data.append({child.tag, str(child.text)})
        # return data
            return child.text

    def get_xml_element_text_array_from_package_database_file(self, xml_file, xml_root, xml_node):
        # def get_xml_node_from_file(self, xml_file, xml_root):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        node = "./"+"".join(xml_root) +"/Package/"+"".join(xml_node) +""
        arry = []
        # node = "./"+"".join(xml_root) +"/Package/"+""
        for child in root.findall(node) :
            # data.append({child.tag, str(child.text)})
        # return data
            arry.append(child.text)
            
        return arry

    