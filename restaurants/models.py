from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import uuid
from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import MaxValueValidator, MinValueValidator

from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase
from taggit.managers import TaggableManager


from tools.models import TimeStampedModel, ActiveManager
from accounts.models import User


# This is the custom "through" model
class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    """
    Because Place PK is UUid it could work with stndart through model of Tag system"""
    # If you need to add any extra fields to the relationship, you can do it here
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        # The following two lines are important for Django 5.0+ and avoid clashes
        # with the default taggit models if you use both integer and UUID PKs.
        app_label = "restaurants" # Or whatever your app is called
        db_table = "restaurants_tagged_items" # Choose a unique table name


class Category(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=300
    )
    slug = models.SlugField(
        allow_unicode=True
    )
    order = models.PositiveSmallIntegerField(
        default=1
    )
    
    class Meta:
        ordering = ['order']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)
    
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
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='places',
        verbose_name=_("category"),
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
        through=UUIDTaggedItem,
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

class Review(TimeStampedModel):
    """
    We could add category relation here but we dont
    because we want a same system of review for any type of place
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        primary_key=True
    )
    name = models.CharField(
        _("Name"),
        max_length=150
    )
    active = models.BooleanField(
        _("Active"),
        default=True
    )
    
    def __str__(self):
        return self.name


class ReviewItem(models.Model):
    class ItemTypeChoice(models.TextChoices):
        FOOD = 'food', _("Food Quality")
        COFFEE = 'coffee', _("Coffee Quality")
        DRINKS = 'drinks', _("Drinks Quality") # tea, juice, cocktail, ..
        MENU_VARIETY = 'menu_variety', _("Menu Variety")
        SERVICE = 'service', _("Service") # staff friendliness, attentiveness, speed, and professionalism 
        AMBIANCE = 'ambiance', _("Ambiance & Atmosphere")
        VALUE = 'value', _("Value for Money") # if the price was fair for the quality of the food and experience
        
        # --- Logistics & Facilities ---
        CLEANLINESS = 'cleanliness', _("Cleanliness Quality")
        LOCATION = 'location', _("Location & Accessibility")
        PARKING = 'parking', _("Parking Availability")
        FACILITY = 'facility', _("Comfort & Facilities Quality") # wc, disabled, ...
        FAMILY_FRIENDLY = 'family_friendly', _("Family Friendliness")
        SUITABILITY_FOR_GROUPS = 'groups', _("Suitability for Groups")
        SUITABILITY_FOR_WORK = 'work', _("Suitability for Working/Studying")
            
    review = models.ForeignKey(        
        Review, 
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_("Review"),
    )
    item_type = models.CharField(
        _("Item Type"),
        max_length=35,
        choices=ItemTypeChoice.choices,
    )
    order = models.PositiveSmallIntegerField(
        _("Order"),
        default=1
    )
    is_applicable = models.BooleanField(
        _("Is Applicable"),
        default=True,
        help_text=_("Uncheck this if the item is not applicable for this review (e.g., no coffee).")
    )
    description = models.TextField(
        ("Description"),
        blank=True,
    )
    
    class Meta:
        ordering = ('order', )
        unique_together = ('review', 'item_type')
        verbose_name=_("Review Item")
        verbose_name_plural=_("Review Items")
        
    def __str__(self):
        return f'{self.get_item_type_display()} Review'


class Vote(TimeStampedModel):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name=_("Review"),
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name=_("Place"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name=_("User"),
    )

    class Meta:
        unique_together = ('user', 'review', 'place')  # Ensure a user only votes once per review
        # unique_together = ('user', 'review', 'place')  # Ensure a user only votes once per review

    def __str__(self):
        return f'Vote by {self.user.username} on {self.review.name}'


class VoteResponse(models.Model):
    vote = models.ForeignKey(
        Vote, 
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name=_("Vote"),
    )
    review_item = models.ForeignKey(
        ReviewItem, 
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name=_("Review Item"),
    )
    is_applicable = models.BooleanField(
        _("Is Applicable"),
        default=True,
        help_text=_("Uncheck this if the item is not applicable for this review (e.g., no coffee)")
    )
    score = models.PositiveSmallIntegerField(
        _("Score"),
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(5)
            ],
    )
    extra_notes = models.TextField(
        _("Extra notes"),
        blank=True,
        help_text=_("If the item needs any extra details, mention them as short as possible")
    )
    
    # in some cases we could let user edit their review by a boolean field
    class Meta:
        ordering = ('review_item__order',)
        verbose_name = _("Vote Response")
        verbose_name_plural = _("Vote Responses")
        
    def __str__(self):
        return f'Response for {self.vote} on {self.review_item}'