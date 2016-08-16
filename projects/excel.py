from os.path import exists, join
import zipfile

import xlsxwriter

class Excel:

    def __init__(self, table_name, columns, data):
        self.columns = [{'header': col} for col in columns]
        self.data = data
        self.table_name = table_name
        self.main()

    def main(self):        
        file_path = 'frontend/static/'
        self.filename = join(file_path, self.table_name +'.zip')
         
        excel_filename = join(file_path, self.table_name + '.xlsx')
        workbook = xlsxwriter.Workbook(excel_filename)
        worksheet = workbook.add_worksheet(self.table_name)
        excel_data = []
        for row in self.data:
            excel_row = []
            for col in self.columns:
                if col.get('header') in row: 
                    excel_row.append(row.get(col.get('header')))
            excel_data.append(excel_row)

        worksheet.add_table(0, 0, len(excel_data), len(self.columns)-1,
                            {'data': excel_data,
                             'columns': self.columns})
        workbook.close()
        zip = ZipFile(archive_filename, 'w')
        zip.write(excel_filename, arcname=self.table_name + '.xlsx')
        zip.close()
