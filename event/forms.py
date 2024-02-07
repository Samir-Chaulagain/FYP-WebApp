from django import forms
from .models import Booking,saved_event


class EventSavedForm(forms.ModelForm):
    class Meta:
        model = saved_event
        fields = ['event']

class EventBooked(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['num_tickets']
        widgets = {
            'num_tickets': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_num_tickets(self):
        num_tickets = self.cleaned_data['num_tickets']
        if num_tickets <= 0:
            raise forms.ValidationError("Number of tickets must be greater than zero.")
        return num_tickets
    
class EventEditForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['num_tickets']
        widgets = {
            'num_tickets': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_num_tickets(self):
        num_tickets = self.cleaned_data['num_tickets']
        if num_tickets <= 0:
            raise forms.ValidationError("Number of tickets must be greater than zero.")
        return num_tickets