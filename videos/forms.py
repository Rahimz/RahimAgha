from django import forms

from .models import Video, Category

class VideoUploadForm(forms.Form):
    your_file = forms.FileField()
    name = forms.CharField(max_length=150)

class VideoUploadNewForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name', 'video_file', 'category', 'is_protected']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']