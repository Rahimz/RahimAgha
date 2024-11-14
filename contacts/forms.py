from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Contact

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
    
    class Meta:
        model = Contact
        fields = ("title","description","email", "phone", )
        labels = {
            "title": _("Tilte"),
            "description": _("Description"),
            "email": _("Email"),
            "phone": _("Phone"),
        }
   