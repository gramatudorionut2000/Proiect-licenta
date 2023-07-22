from django.db import models
from django.contrib.auth.models import Group
from django.utils import timezone
from django.urls import reverse
from Users.models import CustomUser
import os
from django.conf import settings
import shutil


class Folder(models.Model):
    name=models.CharField(max_length=30)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} {self.name} Folder'
    
    def delete(self):
        user=self.user
        groups=user.groups.all()
        for group in groups:
            path='media/documents/{0}/{1}/{2}'.format(group.name, user.username, self.name)
            shutil.rmtree(path,ignore_errors=True)
        super(Folder, self).delete()

class Tag(models.Model):
    name = models.TextField(max_length=255)

    def __str__(self):
        return f'{self.name}'



class Document(models.Model):

    def filename(self):
        filename=os.path.basename(self.document.name)
        return filename
        
    def get_upload_path(instance,filename):
        return 'documents/{0}/{1}/{2}/{3}'.format(instance.group.name,instance.author.username, instance.folder.name, filename)

    @property
    def get_extension(self):
        name ,extension = os.path.splitext(self.document.name)
        return extension.lower().replace('.', '')


    @property
    def get_name(self):
        name ,extension = os.path.splitext(self.document.name)
        return name   

    def get_absolute_url(self):
        return reverse('document-detail', kwargs={'pk': self.pk})


    description=models.TextField(max_length=500,)
    short_description=models.TextField(max_length=100,)
    date_posted=models.DateTimeField(default=timezone.now)
    name=models.TextField(max_length=255,)
    extension=models.CharField(max_length=5,)
    author=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    folder=models.ForeignKey(Folder, on_delete=models.CASCADE)
    group=models.ForeignKey(Group, on_delete=models.CASCADE)
    tags=models.ManyToManyField(Tag, blank=True)
    document = models.FileField(upload_to=get_upload_path)
    blacklist= models.ManyToManyField(CustomUser, blank=True, related_name='+')
    is_global= models.BooleanField()

    def __str__(self):
        return f'{self.author.username} {self.name}  Document'

    def save(self, *args, **kwargs):
        if self.name == '':
            self.name=self.get_name
        if self.extension == '':
            self.extension=self.get_extension
        super(Document, self).save(*args, **kwargs)

