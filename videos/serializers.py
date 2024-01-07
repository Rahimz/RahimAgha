from rest_framework import serializers

from .models import Video
from .forms import VideoUploadForm


class YourFileSerializer(serializers.Serializer):
    your_file = serializers.FileField()
    def update(self, instance, validated_data):
        pass 

    def create(self, validated_data):
        form = VideoUploadForm(validated_data)
        if form.is_valid():
            return form.cleaned_data['your_file']
    # class Meta:
    #     model = Video
    #     fields = [''