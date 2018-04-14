from io import BytesIO
import warnings

from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage
from django.db import transaction
from django.urls import reverse

from .models import DBFile


class DBFilesStorage(Storage):

    def __init__(self, connection=None):
        self.connection = (connection or
                           getattr(settings, 'DBFILES_CONNECTION', 'default'))

    def __eq__(self, other):
        return self.connection == other.connection

    def deconstruct(self):
        # Required for using as storage in fields
        return (
            self.__class__.__module__ + '.' + self.__class__.__name__,
            (self.connection,),
            {},
        )

    @property
    def _objects(self):
        return DBFile.objects.using(self.connection)
    
    def _open(self, name, mode='rb'):
        if mode!='rb':
            raise NotImplementedError("DBFiles can only be read as 'rb'")
        try:
            f = self._objects.get_for_read(name)
        except DBFile.DoesNotExist:
            return None
        else:
            content = f.content
            fh = BytesIO(content)
            fh.name = name
            fh.mode = mode
            fh.size = len(content)
            if f.size != fh.size:
                warnings.warn("DBFile named {name} needed its size fixed "
                              "from {dbsize} to {size} when read".
                              format(name=name, dbsize=f.size, size=fh.size))
                f.size = fh.size
                f.save()
            return File(fh)

    def _save(self, name, content):
        with transaction.atomic(using=self.connection):
            f = self._objects.get_for_write(name)
            c = content.read()
            f.content = c
            f.size = len(c)
            if len(c) != content.size:
                warnings.warn("DBFile named {name} needed its size fixed "
                              "from {fsize} to {size} when saved".
                              format(name=name, fsize=content.size, size=f.size))
            f.save()
            return name

    def exists(self, name):
        return self._objects.file_exists(name)

    def delete(self, name):
        self._objects.delete_file(name)

    def listdir(self, name):
        # Left here for completeness, and possible future implementation
        return super().listdir(name)

    def size(self, name):
        return self._objects.get_for_properties(name).size

    def url(self, name):
        return reverse('dbfiles_file', kwargs={'name': name})

    def get_accessed_time(self, name):
        # Left here for completeness, and possible future implementation
        return super().get_accessed_time(name)

    def get_created_time(self, name):
        return self._objects.get_for_properties(name).created_time

    def get_modified_time(self, name):
        return self._objects.get_for_properties(name).modified_time
