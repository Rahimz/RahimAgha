from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import FileSystemStorage
import uuid 

from quizes.models import TimeStampedModel

class CustomStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # Customize the file name if needed
        return super().get_available_name(name, max_length)

custom_storage = CustomStorage(location='private_media/videos/')
    

class Category(TimeStampedModel):
    name = models.CharField(
        _('Name'),
        max_length=200,        
    )
    
    def __str__(self):
        return self.name


class Video(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='videos'
    )
    video_file = models.FileField(
        _('Video file'), 
        upload_to='videos/',

    )
    name = models.CharField(
        max_length=200,
        default='test'
    )

    def get_download_info(self):
        _file = self.video_file
        # content_type = "audio/mp3"
        # download_name = self.name + ".mp3"
        return _file # content_type, download_name, 
    is_protected = models.BooleanField(default=False)
    website_header = models.CharField(
        max_length=200,
        default='',
        blank=True,
    )
    def __str__(self):
        return self.name
    
    def get_size(self):
        if self.is_protected:
            return custom_storage.size(self.video_file.name)
        else:
            return self.video_file.size
        
    def save(self, *args, **kwargs):
        if self.website_header:
            self.is_protected = True
        if self.is_protected:
            self.video_file.storage = custom_storage
        super().save(*args, **kwargs)
  

