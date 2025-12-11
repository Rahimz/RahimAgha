from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from parler.managers import TranslatableManager
import uuid

from tools.models import TimeStampedModel, ActiveManager


class ActiveManagerTranslatable(TranslatableManager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Role(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(
            _("Title"),
            max_length=150,
            unique=True
        ),
    )
    slug = models.SlugField(
        allow_unicode=True
    )
    
    def __str__(self):
        return self.safe_translation_getter('title', str(self.title))
    

class Colleague(TranslatableModel):
    translations = TranslatedFields(
        first_name = models.CharField(
            _("First name"),
            max_length=150,
        ),
        last_name = models.CharField(
            _("Last name"),
            max_length=150,
        ),
    )
    link = models.UUIDField(
        _("Link"),
        null=True,
        blank=True
    )
    roles = models.ManyToManyField(
        Role,
    )
    
    def __str__(self):
        return self.safe_translation_getter('last_name', str(self.last_name))


class ProjectCategory(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(
            max_length=150,
            unique=True
        ),
    )
    slug = models.SlugField(
        _("Slug"),
        allow_unicode=True
    )
    
    def __str__(self):
        return self.safe_translation_getter('name', str(self.name))
    
    
class Project(TranslatableModel, TimeStampedModel):
    translations = TranslatedFields(
        name = models.CharField(
            max_length=150,
            unique=True
        ),
        description = models.TextField(
            _("Description"),
            blank=True
        )
    )
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects',
    )
    slug = models.SlugField(
        _("Slug"),
        allow_unicode=True
    )
    link = models.URLField(
        _("Link"),
        null=True,
        blank=True
    )
    cover_image = models.ImageField(
        _("Cover image"),
        upload_to='projects/covers/',
        null=True,
        blank=True
    )
    colleagues = models.ManyToManyField(        
        Colleague,
        verbose_name=_("Colleagues"),
    )
    active = models.BooleanField(
        _("Active"),
        default=True
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    objects = TranslatableManager()
    actives = ActiveManagerTranslatable()
    
    def __str__(self):
        return self.safe_translation_getter('name', str(self.name))
    

class Image(TimeStampedModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='images',
    )
    file = models.ImageField(
        upload_to='projets/'
    )
    alt_image = models.CharField(
        _("Alt image"),
        max_length=200,
        null=True,
        blank=True
    )