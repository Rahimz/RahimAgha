from django import forms
from django.utils.translation import gettext_lazy as _
from decimal import Decimal, ROUND_HALF_UP
from .models import Place

class PlaceAdminForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'

    def clean_latitude(self):
        lat = self.cleaned_data.get('latitude')
        try:
            if lat is not None:
                # Round the value to 6 decimal places before it gets validated
                precision = Decimal('0.000001')
                return Decimal(lat).quantize(precision, rounding=ROUND_HALF_UP)
        except:
            raise forms.ValidationError(_("The value is not valid"))
        return lat

    def clean_longitude(self):
        lon = self.cleaned_data.get('longitude')
        try:
            if lon is not None:
                # Round the value to 6 decimal places
                precision = Decimal('0.000001')
                return Decimal(lon).quantize(precision, rounding=ROUND_HALF_UP)
        except:
            raise forms.ValidationError(_("The value is not valid"))            
        return lon
