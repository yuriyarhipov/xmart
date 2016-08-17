from pyunpack import Archive
from tempfile import mkdtemp
from projects.gpeh import Gpeh
import os
from django.db import connection
from projects.models import WorkFiles, Projects, Tables
from projects.nokia import Nokia
from projects.ericsson import Ericsson
from projects.huawei import HuaweiWCDMA, HuaweiConfig

class ExcelFile:


    def main(self):
        tables = []

        self.tables.sort()
        excel_name = 'topology'
        if self.filename:
            excel_name = self.filename

        static_path = settings.STATICFILES_DIRS[0]
        archive_filename = join(static_path, excel_name +'.zip')
        excel_filename = join(tempfile.mkdtemp(), excel_name + '.xlsx')
        workbook = xlsxwriter.Workbook(excel_filename)
        for table in self.tables:
            sql = "SELECT * FROM " + table + "  WHERE (project_id='" + str(self.project.id) + "');"
            cursor.execute(sql)
            columns = [{'header':'%s' % desc[0]} for desc in cursor.description]
            data = cursor.fetchall()
            worksheet = workbook.add_worksheet(table)
            worksheet.add_table(
                0,
                0,
                len(data),
                len(columns) - 1,
                {'data': data,
                 'columns': columns})
        workbook.close()
    
        zip = ZipFile(archive_filename, 'w')
        zip.write(excel_filename, excel_name + '.xlsx')
        zip.close()

class Parser:

    def unpuck_files(self, filename):
        result_path = mkdtemp(suffix='_xmart')
        Archive(filename).extractall(result_path)
        result = []
        return [os.path.join(path, file)
            for (path, dirs, files) in os.walk(result_path)
            for file in files]

    def parse_file(self, uploaded_file):
        print('Parser')
        connection.close()
        unpacked_files = self.unpuck_files(uploaded_file.filename)

        if uploaded_file.filetype == 'Gpeh':
            for f in unpacked_files:
                gp = Gpeh().parse_file(f)
                WorkFiles.objects.create(
                    project = uploaded_file.project,
                    filename = uploaded_file.filename,
                    description = uploaded_file.description,
                    network = uploaded_file.network,
                    filetype = uploaded_file.filetype,
                    vendor = uploaded_file.vendor,
                    result = os.path.basename(gp)
                )
        elif uploaded_file.vendor == 'Nokia':
            wf = WorkFiles.objects.create(
                project = uploaded_file.project,
                filename = uploaded_file.filename,
                description = uploaded_file.description,
                network = uploaded_file.network,
                filetype = uploaded_file.filetype,
                vendor = uploaded_file.vendor,
                result = ''
            )
            for f in unpacked_files:
                nokia = Nokia(f)
                for table, data in nokia.data.items():
                    print(table)
                    Tables.objects.create(
                        workfile = wf,
                        vendor = 'Nokia',
                        network = uploaded_file.network,
                        table = table,
                        data = data,
                    )
            print('finish nokia')

        elif uploaded_file.vendor == 'Ericsson':
            wf = WorkFiles.objects.create(
                project = uploaded_file.project,
                filename = uploaded_file.filename,
                description = uploaded_file.description,
                network = uploaded_file.network,
                filetype = uploaded_file.filetype,
                vendor = uploaded_file.vendor,
                result = ''
            )
            for f in unpacked_files:
                ericsson = Ericsson(f)
                for table, data in ericsson.data.items():
                    Tables.objects.create(
                        workfile = wf,
                        vendor = uploaded_file.vendor,
                        network = uploaded_file.network,
                        table = table,
                        data = data,
                    )


        elif uploaded_file.vendor == 'Huawei':
            wf = WorkFiles.objects.create(
                project = uploaded_file.project,
                filename = uploaded_file.filename,
                description = uploaded_file.description,
                network = uploaded_file.network,
                filetype = uploaded_file.filetype,
                vendor = uploaded_file.vendor,
                result = ''
            )
            for f in unpacked_files:
                if '.xml' in f:
                    hw = HuaweiWCDMA(f)
                else:
                    hw = HuaweiConfig(f)
                for table, data in hw.data.items():
                    Tables.objects.create(
                        workfile = wf,
                        vendor = uploaded_file.vendor,
                        network = uploaded_file.network,
                        table = table,
                        data = data,
                    )


        uploaded_file.delete()
