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

    def save(self, user):
        # Create the Vote and VoteResponse objects when the form is saved

        # 1. Create the main Vote object
        vote = Vote.objects.create(
            user=user,
            review=self.review
        )

        # 2. Create a VoteResponse for each ReviewItem
        for item in self.review.items.all():
            VoteResponse.objects.create(
                vote=vote,
                review_item=item,
                score=self.cleaned_data[f'score_{item.id}'],
                extra_notes=self.cleaned_data[f'extra_notes_{item.id}']
            )

        return vote