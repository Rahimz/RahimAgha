from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid 

from quizes.models import TimeStampedModel


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
        max_length=10,
        default='test'
    )

    def get_download_info(self):
        _file = self.video_file
        # content_type = "audio/mp3"
        # download_name = self.name + ".mp3"
        return _file # content_type, download_name, 

    



