from django import forms
from .models import Dispute

class ContactForm(forms.Form):
        name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Your Name'})
    )
        email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Your Email'})
    )
        subject = forms.CharField(
        max_length=200, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Subject'})
    )
        message = forms.CharField(
        required=True, 
        widget=forms.Textarea(attrs={'placeholder': 'Your Message'})
    )
class DisputeForm(forms.ModelForm):
    class Meta:
        model = Dispute
        fields = ['name', 'email', 'invoice', 'issue']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'invoice': forms.TextInput(attrs={'placeholder': 'Invoice'}),
            'issue': forms.Textarea(attrs={'placeholder': 'Your Message'})
        }
