from django import forms


class VideoUploadForm(forms.Form):
    your_file = forms.FileField()
    name = forms.CharField(max_length=150)