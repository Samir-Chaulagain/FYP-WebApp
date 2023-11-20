from django import forms
from explore.models import *



class additemForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['name'].label = "Item Name :"
        self.fields['instrument_brand'].label = "Instrument Brand :"
        self.fields['instrument_model'].label = "Instrument Model :"
        self.fields['category'].label = "Category :"
        self.fields['description'].label = "Description :"
        
        self.fields['price'].label = "Price :"
        self.fields['instrument_image1'].label = "Instrument Image 1 :"
        self.fields['instrument_image2'].label = "Instrument Image 2 :"
        self.fields['instrument_image3'].label = "Instrument Image 3 :"
        

        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Enter item name',
            }
        )
        self.fields['instrument_brand'].widget.attrs.update(
            {
                'placeholder': 'Enter instrument brand',
            }
        )
        self.fields['instrument_model'].widget.attrs.update(
            {
                'placeholder': 'Enter instrument model',
            }
        )
        self.fields['description'].widget.attrs.update(
            {
                'placeholder': 'Enter item description',
            }
        )
        self.fields['price'].widget.attrs.update(
            {
                'placeholder': 'Enter item price',
            }
        )
          


    class Meta:
        model = Item
        fields = [
            "category",
            "name",
            "description",
            "instrument_model",
            "item_type",
            "instrument_brand",
            "price",
            "instrument_image1",
            "instrument_image2",
            "instrument_image3",
        ]

    def clean_item_type(self):
        item_type = self.cleaned_data.get('item_type')

        if not item_type:
            raise forms.ValidationError("Item_type is required")
        return item_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("category is required")
        return category


    def save(self, commit=True):
        item = super(additemForm, self).save(commit=False)
        if commit:
            
            item.save()
        return item



class instrument_rent(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['item']

class saveitem(forms.ModelForm):
    class Meta:
        model = saved_item
        fields = ['item']




class edititemForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['name'].label = "Item Name :"
        self.fields['instrument_brand'].label = "Instrument Brand :"
        self.fields['instrument_model'].label = "Instrument Model :"
        self.fields['category'].label = "Category :"
        self.fields['description'].label = "Description :"
        
        self.fields['price'].label = "Price :"
        self.fields['instrument_image1'].label = "Instrument Image 1 :"
        self.fields['instrument_image2'].label = "Instrument Image 2 :"
        self.fields['instrument_image3'].label = "Instrument Image 3 :"
       

        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Enter item name',
            }
        )
        self.fields['instrument_brand'].widget.attrs.update(
            {
                'placeholder': 'Enter instrument brand',
            }
        )
        self.fields['instrument_model'].widget.attrs.update(
            {
                'placeholder': 'Enter instrument model',
            }
        )
        self.fields['description'].widget.attrs.update(
            {
                'placeholder': 'Enter item description',
            }
        )
        self.fields['price'].widget.attrs.update(
            {
                'placeholder': 'Enter item price',
            }
        )
        self.fields['created_by'].widget.attrs.update(
            {
                'placeholder': 'Enter creator name',
            }
        )   


    class Meta:
        model = Item
        fields = [
            "category",
            "name",
            "description",
            "instrument_model",
            "item_type",
            "instrument_brand",
            "price",
            "instrument_image1",
            "instrument_image2",
            "instrument_image3",
        ]


    def clean_item_type(self):
        item_type = self.cleaned_data.get('item_type')

        if not item_type:
            raise forms.ValidationError("Item required")
        return item_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("Category is required")
        return category


    def save(self, commit=True):
        item = super(edititemForm, self).save(commit=False)
      
        if commit:
            item.save()
        return item

