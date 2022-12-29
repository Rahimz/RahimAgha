from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )
    class Meta:
        abstract = True


class Feature(TimeStampedModel):
    title = models.CharField(
        max_length=100,
    )
    description = models.TextField()
    tags = models.CharField(
            max_length=200,
            null=True,
            blank=True
    )
    show_rank = models.PositiveIntegerField(
        default=10
    )

    class Meta:
        ordering = ('show_rank', 'id')

    def __str__(self):
        return self.title


class Image(models.Model):
    feature = models.ForeignKey(
        'Feature',
        on_delete=models.CASCADE,
        related_name='feature_images',
    )
    title = models.CharField(
        max_length=150,
    )
    image = models.ImageField(
        upload_to='images/'
    )
    image_alt = models.CharField(
        max_length=150,
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return self.title


class Point(models.Model):
    feature = models.ForeignKey(
        'Feature',
        on_delete=models.CASCADE,
        related_name='feature_points',
    )
    content = models.TextField()

    def __str__(self):
        return self.content[:25]