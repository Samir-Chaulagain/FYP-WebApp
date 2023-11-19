from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['num_tickets']

    def clean_num_tickets(self):
        num_tickets = self.cleaned_data['num_tickets']
        if num_tickets <= 0:
            raise forms.ValidationError("Number of tickets must be greater than zero.")
        return num_tickets
