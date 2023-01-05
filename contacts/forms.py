from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Contact

class ContactForm(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = ("title","description", "phone", "email")
        labels = {
            "title": _("Tilte"),
            "description": _("Description"),
            "email": _("Email"),
            "phone": _("Phone"),
        }
