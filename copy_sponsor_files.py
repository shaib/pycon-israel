#!/usr/bin/env python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ilpycon.settings'

import django
django.setup()
from django.core.files.storage import default_storage

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    filesys_prefix = os.path.join(PROJECT_ROOT, 'static/dist/images/sponsor-logos')
    for root, directories, filenames in os.walk(filesys_prefix):
        # print('----', root, '----')
        dir_prefix = root[len(filesys_prefix):]
        outpath = 'sponsor_files' + dir_prefix
        for filename in filenames:
            infile = os.path.join(root, filename)
            outfile = '/'.join([outpath, filename])
            print('     ', filename, '->', outfile)
            with default_storage.open(outfile, 'wb') as f:
                blob = open(infile, 'rb').read()
                f.write(blob)
