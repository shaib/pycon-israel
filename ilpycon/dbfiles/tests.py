import warnings
from io import BytesIO

from django.test import TestCase

from .models import DBFile
from .storage import DBFilesStorage

class StorageTestCase(TestCase):

    def setUp(self):
        self.storage = DBFilesStorage()

    def testBasicSave(self):
        buff = bytes('0123456789', encoding='utf-8')
        content = BytesIO(buff)
        self.storage.save('test_file', content)
        dbf = DBFile.objects.get(name='test_file')
        self.assertEqual(dbf.content, buff)
        self.assertEqual(dbf.size, 10)

    def testBinarySave(self):
        buff = bytes(range(255, -1, -1))
        content = BytesIO(buff)
        self.storage.save('test_file', content)
        dbf = DBFile.objects.get(name='test_file')
        self.assertEqual(dbf.content, buff)
        self.assertEqual(dbf.size, 256)

    def testPathSave(self):
        buff = bytes('0123456789', encoding='utf-8')
        content = BytesIO(buff)
        path = self.storage.generate_filename('path/ test file ')
        self.storage.save(path, content)
        dbf = DBFile.objects.get(name='path/test_file')
        self.assertEqual(dbf.content, buff)
        self.assertEqual(dbf.size, 10)

    def testOpen(self):
        buff = bytes('0123456789', encoding='utf-8')
        DBFile.objects.create(content=buff, name='test_buff', size=10)
        f = self.storage.open('test_buff')
        self.assertEqual(f.size, 10)
        self.assertEqual(f.read(), buff)

    def testOpenFixesSize(self):
        buff = bytes('0123456789', encoding='utf-8')
        DBFile.objects.create(content=buff, name='test_buff', size=9)
        with self.assertWarnsRegex(UserWarning, 'fixed.*when read'):
            f = self.storage.open('test_buff')
        self.assertEqual(f.size, 10)
        self.assertEqual(f.read(), buff)
        dbf = DBFile.objects.get_for_properties('test_buff')
        self.assertEqual(dbf.size, 10)
        

