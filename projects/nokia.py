from lxml import etree


class Nokia():

    data = {}
    filename = ''

    def __init__(self, filename):
        self.filename = filename
        self.from_xml()

    def get_data(self, elem):
        result = dict()
        for param in elem:
            if param.tag == '{raml20.xsd}p':
                p_name = param.get('name')
                if p_name:
                    result[p_name] = param.text
        return result

    def from_xml(self):
        context = etree.iterparse(
            self.filename,
            events=('end',),
            tag='{raml20.xsd}managedObject')
        tables = set()

        context = etree.iterparse(
            self.filename,
            events=('end',),
            tag='{raml20.xsd}managedObject')
        for event, elem in context:
            table_name = elem.get('class')
            mo = elem.get('distName')
            tables.add(table_name)
            row = self.get_data(elem)
            row['mo'] = mo
            mo = print(mo)
            if table_name in self.data:
                self.data[table_name].append(row)
            else:
                self.data[table_name] = [row]
