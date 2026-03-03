from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    # Added hidden fields for Geotagging
    latitude = forms.DecimalField(widget=forms.HiddenInput(), required=False)
    longitude = forms.DecimalField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Complaint
        fields = ['name', 'email', 'subject', 'description', 'photo', 'latitude', 'longitude']