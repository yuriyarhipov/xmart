import re
from lxml import etree


class HuaweiConfig:
    data = dict()

    def __init__(self, filename):
        self.filename = filename
        self.from_file()

    def get_row(self, data):
        result = dict()
        for v in data.split(','):
            key, value = v.split('=')
            key = key.strip().replace(';', '')
            value = value.strip().replace(';', '')
            value = value.strip().replace('"', '')
            result[key] = value
        return result

    def from_file(self):
        with open(self.filename) as f:
            for row in f:
                if (row[:2] != '//') and (':' in row):
                    system_info, data_row = row.split(':')
                    table_name = system_info.split()[1]
                    data_row = self.get_row(data_row)
                    if table_name in self.data:
                        self.data[table_name].append(data_row)
                    else:
                        self.data[table_name] = [data_row, ]
                        

class HuaweiWCDMA:
    xml_mask = re.compile('\{.*\}')
    data = dict()

    def __init__(self, filename):
        self.filename = filename
        self.from_xml()

    def get_params(self, node):
        result = dict()
        for child in node:
            if child.tag != etree.Comment:
                param_name = '_%s' % self.xml_mask.sub('', child.tag)
                if child.text:
                    param_value = child.text.strip()
                    if param_value:
                        result[param_name] = str(param_value)
                child_result = self.get_params(child)
                if child_result:
                    result.update(child_result)
        return result

    def parse_class(self, nermversion, compatibleNrmVersion, node):
        for child in node:
            table_name = self.xml_mask.sub('', node.find('*').tag)
            row = self.get_params(child)
            row['nermversion'] = str(nermversion)
            row['compatibleNrmVersion'] = str(compatibleNrmVersion)
            if row:
                if table_name in self.data:
                    self.data[table_name].append(row)
                else:
                    self.data[table_name] = [row, ]

    def parse_node(self, node):
        nermversion = node.get('nermversion')
        compatibleNrmVersion = ''
        for child in node:
            if 'compatibleNrmVersionList' in child.tag:
                compatibleNrmVersion = etree.tostring(child, method="text").strip()
            elif (child.tag == '{http://www.huawei.com/specs/bsc6000_nrm_forSyn_collapse_1.0.0}class'):
                self.parse_class(nermversion, compatibleNrmVersion, child)

    def from_xml(self):
        context = etree.iterparse(
            self.filename,
            events=('end',),
            tag='{http://www.huawei.com/specs/huawei_wl_bulkcm_xml_baseline_syn_1.0.0}syndata')
        for _, elem in context:
            self.parse_node(elem)
