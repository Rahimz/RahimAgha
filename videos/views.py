from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.views.generic import View
from django.conf import settings
import os


from django.http import StreamingHttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views import View
import mimetypes


from .models import Video

def VideoListView(request):
    videos = Video.objects.all()
    return render (
        request,
        'videos/videos_list.html',
        {
            'videos':videos,
        }
    )



class ProtectedMediaView(View):
    def get(self, request, uuid):
        # Check user permissions or any other access control logic here
        if not request.user.has_perm('can_access_media'):
            return HttpResponseForbidden("You don't have permission to access this media.")

        # Construct the full path to the media file
        media_path = os.path.join(settings.MEDIA_ROOT, str(uuid))

        video = Video.objects.get(id=uuid)

        # Serve the file
        with open(video.video_file.path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')

        return response


def video_details(request, uuid):
    video = Video.objects.get(id=uuid)
    return render(
        request,
        'videos/video_details.html',
        {
            'video':video,
        }
    )



class VideoStreamView(View):
    def get(self, request, *args, **kwargs):
        # Get your video file path or content
        # video_path = "path/to/your/video.mp4"  # Replace with your actual file path or content retrieval logic
        video = Video.objects.get(id=kwargs['uuid'])
        video_path = video.video_file.path
        # Set the correct content type
        content_type, encoding = mimetypes.guess_type(video_path)
        content_type = content_type or 'application/octet-stream'

        # Set response headers to prevent direct download
        response = StreamingHttpResponse(self.file_iterator(video_path), content_type=content_type)
        response['Content-Disposition'] = 'inline; filename="video.mp4"'  # Set filename for inline display

        return response

    def file_iterator(self, file_path, chunk_size=8192):
        with default_storage.open(file_path, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data