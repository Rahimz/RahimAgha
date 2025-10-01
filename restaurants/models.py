from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import uuid
from decimal import Decimal, ROUND_HALF_UP

from taggit.managers import TaggableManager


from tools.models import TimeStampedModel, ActiveManager


class Place(TimeStampedModel):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False,
    )
    name = models.CharField(
        _("Name"),
        max_length=300
    )
    slug = models.SlugField(
        allow_unicode=True
    )
    description = models.TextField(
        blank=True,
    )
    
    
    city = models.CharField(
        _("City"),
        max_length=150,
    )
    address = models.TextField(
        _("Address"),
        blank=True
    )
    latitude = models.DecimalField(
        max_digits=9,  # Total number of digits
        decimal_places=6,  # Number of digits after the decimal point
        help_text=_("Latitude in decimal degrees (e.g., -90.000000 to 90.000000)"),
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=10,  # Total number of digits
        decimal_places=6,  # Number of digits after the decimal point
        help_text=_("Longitude in decimal degrees (e.g., -180.000000 to 180.000000)"),
        null=True,
        blank=True,
    )
    score = models.PositiveSmallIntegerField(
        _("Score"),
        default=0
    )
    
    tags = TaggableManager(
        _("Tags"),        
        blank=True
    )
    
    active = models.BooleanField(
        _("Active"),
        default=True,
        )
    objects = models.Manager()
    actives = ActiveManager()
    
    class Meta:
        verbose_name = _("Place")
        verbose_name_plural = _("Places")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        # Round coordinates as a final guarantee of data integrity
        precision = Decimal('0.000001')
        if self.latitude is not None:
            self.latitude = Decimal(self.latitude).quantize(precision, rounding=ROUND_HALF_UP)
        if self.longitude is not None:
            self.longitude = Decimal(self.longitude).quantize(precision, rounding=ROUND_HALF_UP) 
        # Call the original save() method
        return super().save(*args, **kwargs)
    

# images 
# features service option, dinning option, facilities, wc, parking, crowded, 
# reviews
