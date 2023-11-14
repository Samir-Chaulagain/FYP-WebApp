from django import forms
from explore.models import *
class add_item_form(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['name'].label = "name:"        
        self.fields['description'].label = "Item Description :"        
        self.fields['instrument_model'].label = "instrument_model:"
        self.fields['instrument_brand'].label = "instrument_brand:"
        self.fields['price'].label = "price :"
        self.fields['created_by'].label = "Owner :"
        


        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Matras Guitar',
            }
        )        
            
        self.fields['instrument_brand'].widget.attrs.update(
            {
                'placeholder': 'Mantra',
            }
        )
        self.fields['instrument_model'].widget.attrs.update(
            {
                'placeholder': 'Mantra',
            }
        )
        self.fields['price'].widget.attrs.update(
            {
                'placeholder': '500',
            }
        )
                      
            
        


    class Meta:
        model = Item

        fields = [
            "name",
            "instrument_brand",
            "instrument_model",
            "price",
            "description",
            "created_by",
            'category'
            
            ]