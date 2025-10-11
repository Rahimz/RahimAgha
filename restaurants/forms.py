from django import forms
from django.utils.translation import gettext_lazy as _
from decimal import Decimal, ROUND_HALF_UP
from .models import Place, Vote, VoteResponse


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



class ReviewSubmissionForm(forms.Form):
    # We will add fields to this form dynamically in the __init__ method

    def __init__(self, *args, **kwargs):
        # We need the review instance to build the form
        self.review = kwargs.pop('review')
        super().__init__(*args, **kwargs)

        # A choice widget for the score
        SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]

        # Dynamically create fields for each ReviewItem
        for item in self.review.items.all():
            self.fields[f'is_applicable_{item.id}'] = forms.BooleanField(
                initial=True,
                label=_("Is Applicable"),
                required=False,
                help_text=_("Uncheck this if the item is not applicable for this review (e.g., no coffee)")
            )
            # A field for the score (1-5) using radio buttons
            self.fields[f'score_{item.id}'] = forms.ChoiceField(
                label=item.get_item_type_display(),
                choices=SCORE_CHOICES,
                widget=forms.RadioSelect,
                required=True,
                help_text=item.description
            )
            # A field for the optional notes
            self.fields[f'extra_notes_{item.id}'] = forms.CharField(
                label=_("Extra Notes"),
                widget=forms.Textarea(attrs={'rows': 2, 'placeholder': _("Optional notes...")}),
                required=False
            )
    
    
    def clean(self):
        """
        This method handles cross-field validation. We use it to make the 'score'
        field optional if the 'not_applicable' checkbox is checked for that item.
        """
        cleaned_data = super().clean()

        for item in self.review.items.all():
            is_applicable = cleaned_data.get(f'is_applicable_{item.id}')
            score_field_name = f'score_{item.id}'

            if not is_applicable:
                # If marked as not applicable, the score is no longer required.
                # 1. Remove the potential "this field is required" error from the form.
                if score_field_name in self._errors:
                    del self._errors[score_field_name]

                # 2. Set the score in cleaned_data to None for the save method.
                cleaned_data[score_field_name] = None
                
    def save(self, user, place):
        # Create the Vote and VoteResponse objects when the form is saved

        # 1. Create the main Vote object
        vote = Vote.objects.create(
            user=user,
            review=self.review,
            place=place
        )

        # 2. Create a VoteResponse for each ReviewItem
        for item in self.review.items.all():
            VoteResponse.objects.create(
                vote=vote,
                review_item=item,
                is_applicable=self.cleaned_data.get(f'is_applicable_{item.id}', True),
                score=self.cleaned_data[f'score_{item.id}'],
                extra_notes=self.cleaned_data[f'extra_notes_{item.id}']
            )

        return vote