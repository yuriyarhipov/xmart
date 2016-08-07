from pyunpack import Archive
from tempfile import mkdtemp
from projects.gpeh import Gpeh
import os
from django.db import connection
from projects.models import WorkFiles, Projects, Tables
from projects.nokia import Nokia
from projects.ericsson import Ericsson
from projects.huawei import HuaweiWCDMA

class Parser:

    def unpuck_files(self, filename):
        result_path = mkdtemp(suffix='_xmart')
        Archive(filename).extractall(result_path)
        result = []
        return [os.path.join(path, file)
            for (path, dirs, files) in os.walk(result_path)
            for file in files]

    def parse_file(self, uploaded_file):
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
                    Tables.objects.create(
                        workfile = wf,
                        vendor = 'Nokia',
                        network = uploaded_file.network,
                        table = table,
                        data = data,
                    )

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
                hw = HuaweiWCDMA(f)
                for table, data in hw.data.items():
                    Tables.objects.create(
                        workfile = wf,
                        vendor = uploaded_file.vendor,
                        network = uploaded_file.network,
                        table = table,
                        data = data,
                    )


        uploaded_file.delete()
