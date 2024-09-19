from django.db import models



class GeoRecord(models.Model):
    ip = models.GenericIPAddressField()
    created = models.DateTimeField(auto_now_add=True)
    country= models.CharField(
        max_length=10
    )

    def __str__(self):
        return f"{self.country}-{self.ip}"
    
