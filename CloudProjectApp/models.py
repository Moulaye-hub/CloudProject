from django.db import models
from .validators import validate_file_extension
from django.db.models.fields.related import OneToOneField


class FileInitial(models.Model):
    id_file = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='Cloud_Project/')
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.file.name)

class FileProcessed(models.Model):
    id_file_cleared = models.AutoField(primary_key=True)
    file = models.ForeignKey(FileInitial, on_delete=models.CASCADE)
    file_cleared = models.FileField(upload_to='Cloud_Project/')
    
    def __str__(self):
        return str(self.file_cleared.name)