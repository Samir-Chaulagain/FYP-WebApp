from django import forms


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