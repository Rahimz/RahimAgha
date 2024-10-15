from django.db import models



class GeoRecord(models.Model):
    ip = models.GenericIPAddressField()
    created = models.DateTimeField(auto_now_add=True)    
    updated = models.DateTimeField(auto_now=True)    
    country= models.CharField(
        max_length=10
    )
    count = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return f"{self.country}-{self.ip}"
    
