from django import forms
from .models import Complaint, Response, Category

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['category', 'name', 'email', 'phone', 'subject', 'description', 'location', 'attachment']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['responder_name', 'responder_title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class TrackingForm(forms.Form):
    tracking_id = forms.CharField(max_length=20, label="Complaint Tracking ID")