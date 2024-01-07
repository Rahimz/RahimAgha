from celery import shared_task
from .models import Video


@shared_task()
def upload_file(file, name, category):   
    video = Video.objects.create(
        video_file=file, name=name, category=category
    )
