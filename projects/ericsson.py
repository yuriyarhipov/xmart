from lxml import etree
from os.path import basename
import datetime
import re


class Ericsson(object):
    rows = []
    ignored_name = []
    version = ''
    vendorName = ''
    path = re.compile('\{.*\}')
    ver = re.compile('^\D+')
    stop_list = ['ManagementNode', ]
    db_tables = set()
    current = float(1)
    data = dict()

    def __init__(self, filename):
        self.filename = filename
        self.main()

    def parse_mo(self, mo):
        result = dict()
        pattern = '(\w*)=(\w*-*\w*)'
        k = re.compile(pattern)
        for k, v in re.findall(k, mo):
            result[k] = v
        return result

    def get_table_name(self, node):
        table_name = None
        parent = node.getparent()
        if 'VsDataContainer' in parent.tag:
            data = node.find(".//{genericNrm.xsd}vsDataType")
            if data is not None:
                table_name = data.text[6:]
        else:
            table_name = self.path.sub('', parent.tag)
        return table_name

    def get_additional_fields(self, node, table_name):
        result = dict()
        parent = node.getparent()
        if (('VsDataContainer' in parent.tag) and
           (table_name in parent.getparent().tag)):
            for n in parent.getparent():
                if 'attributes' in n.tag:
                    for attr in n:
                        field_name = self.path.sub('', attr.tag)
                        text = getattr(attr, 'text', '')
                        if text is None:
                            text = ''
                        text = text.replace('vsData', '')
                        result[field_name] = text
        return result

    def get_fields(self, node, table_name):
        result = dict()
        result.update(self.get_additional_fields(node, table_name))



        for n in node.iter():
            if 'vsDataFormatVersion' in n.tag:
                result['version'] = self.ver.sub('', n.text)
                self.version = result['version']
            if n.text is None:
                n.text = ''

            parent = n.getparent()
            if (('{genericNrm.xsd}attributes' not in parent.tag) and
               ('vsdata' not in parent.tag.lower())):
                field_name = '%s_%s' % (
                    self.path.sub('', parent.tag),
                    self.path.sub('', n.tag))
            else:
                field_name = self.path.sub('', n.tag)
            text = n.text.strip().replace('vsData', '')
            if (('vsData' not in field_name) and
               (field_name not in ['attributes'])):
                if field_name in result:
                    result[field_name] = '%s %s' % (result[field_name], text)
                else:
                    result[field_name] = text

        if table_name == 'UtranRelation':
            if 'adjacentCell' in result:
                ac = self.parse_mo(result.get('adjacentCell'))
                result['Neighbor'] = ac.get('UtranCell')
        elif table_name == 'IubLink':
            if 'iubLinkNodeBFunction' in result:
                ib = self.parse_mo(result.get('iubLinkNodeBFunction'))
                result['Element2'] = ib.get('MeContext')

        elif table_name == 'SectorEquipmentFunction':
            rb = self.parse_mo(result.get('reservedBy'))
            rf_branch_ref = self.parse_mo(result.get('rfBranchRef'))
            result['EUtranCellFDD'] = rb.get('EUtranCellFDD')
            result['AntennaUnitGroup'] = rf_branch_ref.get('AntennaUnitGroup')

        elif table_name == 'EUtranCellRelation':
            ac = self.parse_mo(result.get('adjacentCell'))
            result['Target'] = ac.get('EUtranCellFDD')
            if 'EUtranCellFDD' not in result:
                result['EUtranCellFDD'] = result['Target']

        elif table_name == 'CoverageRelation':
            tc = self.parse_mo(result.get('utranCellRef'))
            result['Target_coverage'] = tc.get('UtranCell', '')
        return result

    def get_mo(self, node):
        result = []
        parent = node.getparent()
        if parent is not None:
            result = self.get_mo(parent)
        value = node.get('id')
        name = None
        if value is not None:
            tag = self.path.sub('', node.tag)
            if tag == 'VsDataContainer':
                datatype = node.find(".//{genericNrm.xsd}vsDataType")
                if datatype is not None:
                    name = datatype.text[6:]
            else:
                name = tag
            if name and value:
                result.append('%s=%s' % (name, value))
        return result

    def parse_elem(self, elem):
        table_name = self.get_table_name(elem)
        if table_name in self.stop_list:
            return
        fields = self.get_fields(elem, table_name)

        if table_name not in self.data:
            self.data[table_name] = []
        self.data[table_name].append(fields)

    def main(self):
        context = etree.iterparse(
            self.filename,
            events=('end',),
            tag='{genericNrm.xsd}attributes')

        for event, elem in context:
            self.parse_elem(elem)
            elem.clear()
