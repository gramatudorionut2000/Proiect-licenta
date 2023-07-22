from django.db import models
from PIL import Image
from django.contrib.auth.models import AbstractUser
import shutil
class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    
    def delete(self):
        groups=self.groups.all()
        for group in groups:
            path='media/documents/{0}/{1}'.format(group.name, self.username,)
            shutil.rmtree(path,ignore_errors=True)
        super(CustomUser, self).delete()

class Profile(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height>300 or img.width>300:
            output=(300, 300)
            img.thumbnail(output)
            img.save(self.image.path)

