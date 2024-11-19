from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponse
from django.views.generic import View
from django.conf import settings
import os
from django.contrib.admin.views.decorators import staff_member_required


from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import YourFileSerializer
from .forms import VideoUploadForm, VideoUploadNewForm, CategoryForm

from django.http import StreamingHttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views import View
import mimetypes


from .models import Video, Category
from .tasks import upload_file







@staff_member_required
def VideoListView(request, category_id=None):
    category = None
    context = dict(
        page_title='All videos'
    )
    videos = Video.objects.all().order_by('-created')
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
        except: 
            pass
    if category:
        videos = videos.filter(category=category)
        context['page_title'] = f"Category: {category.name}"

    context['videos'] = videos
    return render (
        request,
        'videos/videos_list.html',
        context
    )



class ProtectedMediaView(View):
    def get(self, request, uuid):
        # Check user permissions or any other access control logic here
        if not request.user.has_perm('can_access_media'):
            return HttpResponseForbidden("You don't have permission to access this media.")

        video = Video.objects.get(id=uuid)

        # Construct the full path to the media file
        media_path = os.path.join(settings.MEDIA_ROOT, video.name)


        # Serve the file
        with open(video.video_file.path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')

        return response


@staff_member_required
def video_details(request, uuid):
    video = Video.objects.get(id=uuid)
    return render(
        request,
        'videos/video_details.html',
        {
            'video':video,
        }
    )




def restrict_referer(request, website):
    # Check if the request has a referer
    referer = request.META.get('HTTP_REFERER')
    
    # Define the allowed website
    allowed_website = website
    if website == '':
        return True
    
    # Check if the referer matches the allowed website
    if referer and referer.startswith(allowed_website):
        # If the referer matches, allow the request to continue
        return True
    else:
        # If the referer doesn't match, return a forbidden response
        return False


class VideoStreamView(View):
    def get(self, request, *args, **kwargs):
        video = Video.objects.get(id=kwargs['uuid'])
        website = video.website_header

        
        if restrict_referer(request, website):
            referer = request.META.get('HTTP_REFERER')

            video_path = video.get_path()
            # Set the correct content type
            content_type, encoding = mimetypes.guess_type(video_path)
            content_type = content_type or 'application/octet-stream'

            # Set response headers to prevent direct download
            response = StreamingHttpResponse(self.file_iterator(video_path), content_type=content_type)
            response['Content-Disposition'] = 'inline; filename="video.mp4"'  # Set filename for inline display
            if referer and ('computermuseum.ir' in referer or 'atmancenter.org' in referer):
                response['X-Frame-Options'] = 'ALLOW-FROM ' + referer
            return response
            # return HttpResponse("Allowed")
        else:
            # Return a forbidden response
            return HttpResponseForbidden()


    def file_iterator(self, file_path, chunk_size=8192):
        with default_storage.open(file_path, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data

class AtmanVideoStreamView(View):
    def get(self, request, *args, **kwargs):
        video = Video.objects.get(id=kwargs['uuid'])
        website = video.website_header

        referer = request.META.get('HTTP_REFERER')
        if referer and referer.startswith('https://atmancenter.org/'):
        
            video_path = video.get_path()
            # print(video_path)
            # Set the correct content type
            content_type, encoding = mimetypes.guess_type(video_path)
            content_type = content_type or 'application/octet-stream'

            # Set response headers to prevent direct download
            response = StreamingHttpResponse(self.file_iterator(video_path), content_type=content_type)
            response['Content-Disposition'] = 'inline; filename="video.mp4"'  # Set filename for inline display
            # set the header for request from specific origin
            # response['X-Frame-Options'] = 'ALLOW-FROM https://atmancenter.org' # we set it in nginx
            # This will only allow requests from atmancenter.org to access your video content.
            response['Access-Control-Allow-Origin'] = 'https://atmancenter.org'
            # allow methods
            response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            # specifies the allowed headers for the request
            response['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Range'
            # specifies the headers that are exposed to the client.
            response['Access-Control-Expose-Headers'] = 'Content-Length, Content-Range'
            return response
            # return HttpResponse("Allowed")
        else:
            # Return a forbidden response
            return HttpResponseForbidden()


    def file_iterator(self, file_path, chunk_size=8192):
        with default_storage.open(file_path, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data



class FileUploader(APIView):
    parser_classes = (FileUploadParser,)
    def get(self, request, *args, **kwargs):
        form = VideoUploadForm()
        return render (request, 'videos/video_upload.html', {'form': form})
    def post(self, request, *args, **kwargs):
        file_serializer = YourFileSerializer(data=request.data)

        if file_serializer.is_valid():
            new_file = file_serializer.validated_data['your_file']
            
            vid = Video.objects.create(
                video_file=new_file,
                name=new_file.name
            )
            response = Response({'video_id': vid.id}, status=status.HTTP_201_CREATED)
            response['Content-Disposition'] = f'attachment; filename="{new_file.name}"'
            # response['Content-Disposition'] = f'attachment; filename="{your_file.name}"'
            return response
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class FileUploader(APIView):
    parser_classes = (FileUploadParser,)

    def get(self, request, *args, **kwargs):
        form = VideoUploadForm()
        return render(request, 'videos/video_upload.html', {'form': form})

    def post(self, request, *args, **kwargs):
        file_serializer = YourFileSerializer(data=request.data)
        print(file_serializer)
        # print (request.data)
        if file_serializer.is_valid():
            print('hi')
            new_file = file_serializer.validated_data['your_file']
            name = file_serializer.validated_data['name']
            print(name, new_file.name)
            vid = Video.objects.create(
                video_file=new_file,
                name=new_file.name
            )
            response = Response({'video_id': vid.id}, status=status.HTTP_201_CREATED)
            response['Content-Disposition'] = f'attachment; filename="{name}"'
            return response
        else: 
            print(file_serializer.errors)
        # print(response)
        # print(response.items())
        return Response(file_serializer.errors)
    

@staff_member_required
def NewFileUploader(request):
    if request.method == 'POST':
        form = VideoUploadNewForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_video = form.save(commit=False)
            file = new_video.video_file
            # it wirtes file in root of project
            # handle_uploaded_file(file)
            new_video.save()
            # upload_file.delay(new_video.video_file, new_video.name, new_video.category)
            # add sample comments
            return redirect ('videos:video_list')
    else:
        form = VideoUploadNewForm()
    return render(
        request, 
        'videos/video_upload.html', 
        {'form': form},     
    )


def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@staff_member_required
def AddCategoryView(request):
    if request.method == 'POST':
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect ('videos:video_list')
    else:
        form = CategoryForm()

    context = dict(
        form=form
    )
    return render(
        request,
        'videos/add_category.html',
        context
    )


