from django.db import models


class DBFileQuerySet(models.QuerySet):

    def get_for_read(self, name):
        return super().get(name=name)

    def get_for_properties(self, name):
        return super().defer('content').get(name=name)

    def get_for_write(self, name):
        try:
            return super().select_for_update().defer('content').get(name=name)
        except self.model.DoesNotExist:
            return self.model(name=name)

    def file_exists(self, name):
        return super().filter(name=name).exists()

    def delete_file(self, name):
        return super().filter(name=name).delete()


class DBFile(models.Model):

    name = models.CharField(max_length=255, unique=True)
    content = models.BinaryField()
    size = models.IntegerField()  # to enable access without full read
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    objects = DBFileQuerySet.as_manager()
