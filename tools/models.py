from django.db import models
# from tools.gregory_to_hijri import hij_strf_date, greg_to_hij_date


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)

class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True, status='publish')
     
class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )
    class Meta: 
        abstract = True 
    
    
    def get_fa_created(self):
        return hij_strf_date(greg_to_hij_date(self.created.date()), '%-d %B %Y')
    
    def get_fa_updated(self):
        return hij_strf_date(greg_to_hij_date(self.updated.date()), '%-d %B %Y')

    def save(self, *args, **kwargs):
        """
        Overriding the save method in order to make sure that
        modified field is updated even if it is not given as
        a parameter to the update field argument.
        """
        update_fields = kwargs.get('update_fields', None)
        if update_fields:
            kwargs['update_fields'] = set(update_fields).union({'updated'})

        super().save(*args, **kwargs)