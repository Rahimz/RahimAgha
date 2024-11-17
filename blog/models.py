from django.db import models
from django.conf import settings
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

# from tools.gregory_to_hijry import hij_strf_date, greg_to_hij_date
from tools.models import TimeStampedModel, ActiveManager

class PostCategory(TimeStampedModel):
    parent = models.ForeignKey(        
        'self',
        verbose_name=_("Parent category"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(
        _("Name"),
        max_length=150,
        unique=True,
    )
    slug = models.SlugField(
        max_length=150,
        allow_unicode=True,
    )
    active = models.BooleanField(
        default=True
    )
    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    title = models.CharField(
        max_length=150,        
    )
    slug = models.CharField(
        max_length=160, 
        null=True, 
        blank=True,
    )
    category = models.ForeignKey(
        PostCategory,
        related_name='posts',
        verbose_name=_("Category"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    uuid = models.UUIDField(
        default=uuid.uuid4, 
        editable=False,
        unique=True
    )
    author = models.CharField(
        max_length=150,
        null=True, 
        blank=True,
    )
    show_date = models.DateTimeField(
        null=True, 
        blank=True
    )
    rank = models.IntegerField(
        default=1
    )
    description = models.TextField(
        blank=True
    )
    
    cover_image = models.ImageField(
        null=True, 
        blank=True,
        upload_to='blog/covers/'
    )
    image_alt = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    published = models.BooleanField(
        default=False
    )
    active = models.BooleanField(
        default=True
    )
    objects = models.Manager()
    actives = ActiveManager()
    

    class Meta:
        ordering = ('rank', '-show_date', 'id')
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # slug could be more than one
        self.slug = slugify(self.title, allow_unicode=True)
        if not self.show_date:
            self.show_date = self.created
        return super().save(*args, **kwargs)



class Attachment(models.Model):     
    class AttachType(models.TextChoices):
        TITLE =  'title', _("Title")
        TEXT =  'text', _("Text")
        CODE =  'code', _("Code")
        PDF = 'PDF', _("PDF")
        DOCS = 'DOCS', _("DOCS")
        IMAGE = 'image', _("Image")
        LINK = 'link', _("Link")
        VIDEOFILE = 'video_file', _("Video file")   
        SCRIPT = 'script', _("Script")

    title = models.CharField(
        _("Title"),
        max_length=250,
    )
    uuid = models.UUIDField(
        default=uuid.uuid4, 
        editable=False,
        unique=True
    )
    post = models.ForeignKey(
        Post,
        verbose_name=_("Post"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="attachments"
    ) 
    type = models.CharField(
        max_length=15,
        default=AttachType.PDF,
        choices=AttachType.choices
    )
    text = models.TextField(
        _("Text"),        
        blank=True,
        null=True
    )
    file = models.FileField(
        _("File"),
        upload_to='courses/lessons/',
        blank=True, 
        null=True,
    )    
    url = models.URLField(
        _("Link"),
        null=True,
        blank=True,
    )
    script = models.TextField(
        _("Script"),
        null=True,
        blank=True
    )
    code = models.TextField(
        _("Code"), 
        null=True,       
        blank=True
    )
    rank = models.PositiveSmallIntegerField(
        _("Rank"),
        default=1,
    )    
       
    
    active = models.BooleanField(
        _("Active"),
        default=True
    )    

    class Meta:
        ordering = ('rank',)

    def __str__(self):
        return self.title    
   
    # def save(self, *args, **kwargs):        
    #     return super().save(*args, **kwargs)
