=======
dbfiles
=======

A storage system for Django to store files in the database.

This is generally a bad idea, but in some circumstances where
you can't trust the filesystem (e.g. Heroku) and you don't
expect heavy loads it can be a suitable replacement for
proper solutions.

Usage
=====

``dbfiles.storage.DBFilesStorage`` can be used as a storage
class, either via ``DEFAULT_FILE_STORAGE`` or by passing an
instance as the ``storage`` argument of a ``FileField``.


To do
=====

- Add more tests
- Break out of the project as an independent app

Acknowledgement
===============
Inspired by the django-database-files_ project


.. _django-database-files:  https://github.com/bfirsh/django-database-files
