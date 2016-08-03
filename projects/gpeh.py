import struct
import os
import shutil
from zipfile import ZipFile

class Gpeh:
    data = []
    def parse_file(self, filename):
        result_file = os.path.basename(filename)[:-4]
        os.system('gpeh/GpehPar %s -> gpeh/%s.txt' % (filename, result_file))
        archive_filename = 'frontend/static/%s.zip' % (result_file, )
        zip = ZipFile(archive_filename, 'w')
        zip.write('gpeh/%s.txt' % (result_file, ))
        zip.close()
        return archive_filename
