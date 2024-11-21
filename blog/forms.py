from django import forms

from .models import Post, Attachment


class AddAttachmentTitleForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['title', 'rank']

class AddAttachmentTextForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['title', 'text', 'rank']

class AddAttachmentCodeForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['title', 'code', 'rank']

class AddAttachmentCodeForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['title', 'code', 'rank']

class AddAttachmentImageForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['title', 'file', 'rank']

class AddAttachmentLinkForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['title', 'url', 'rank']

class AddAttachmentScriptForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['title', 'script', 'rank']
        
"""

TITLE =  'title', _("Title")
TEXT =  'text', _("Text")
CODE =  'code', _("Code")
PDF = 'PDF', _("PDF")
DOCS = 'DOCS', _("DOCS")
IMAGE = 'image', _("Image")
LINK = 'link', _("Link")
VIDEOFILE = 'video_file', _("Video file")   
SCRIPT = 'script', _("Script")
"""