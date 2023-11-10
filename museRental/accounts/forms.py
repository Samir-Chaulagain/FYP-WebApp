from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
# from phonenumber_field.formfields import PhoneNumberField
# from django_countries.fields import CountryField


from accounts.models import User

class CustomerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=10, required=True, label='Phone Number',
                                   widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}))
   
    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].label = "First Name :"
        self.fields['last_name'].label = "Last Name :"
        self.fields['password1'].label = "Password :"
        self.fields['password2'].label = "Confirm Password :"
        self.fields['email'].label = "Email :"
        self.fields['phone_number'].label = "Phone Number :"
        self.fields['gender'].label = "Gender :"
        # self.fields['pdf_document'].label = "Upload your CV :"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )
        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Enter Phone Number',
            }
        )
        

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number',  'password1', 'password2', 'gender']

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = UserCreationForm.save(self,commit=False)
        user.role = "customer"
        if commit:
            user.save()
        return user
    
class LessorRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=10, required=True, label='Phone Number',
                                   widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}))
   
    def __init__(self, *args, **kwargs):
        super(LessorRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].label = "First Name :"
        self.fields['last_name'].label = "Last Name :"
        self.fields['password1'].label = "Password :"
        self.fields['password2'].label = "Confirm Password :"
        self.fields['email'].label = "Email :"
        self.fields['phone_number'].label = "Phone Number :"
        self.fields['gender'].label = "Gender :"
        # self.fields['pdf_document'].label = "Upload your CV :"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )
        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Enter Phone Number',
            }
        )
        

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number',  'password1', 'password2', 'gender']

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = UserCreationForm.save(self,commit=False)
        user.role = "lessor"
        if commit:
            user.save()
        return user
  





class CustomerLoginForm(forms.Form):
    email =  forms.EmailField(
    widget=forms.EmailInput(attrs={ 'placeholder':'Email',})
) 
    password = forms.CharField(strip=False,widget=forms.PasswordInput(attrs={
        
        'placeholder':'Password',
    }))
    def __init__(self, request=None, *args, **kwargs):
        super(CustomerLoginForm, self).__init__(request, *args, **kwargs)

   
class lessorLoginForm(forms.Form):
    email =  forms.EmailField(
    widget=forms.EmailInput(attrs={ 'placeholder':'Email',})
) 
    password = forms.CharField(strip=False,widget=forms.PasswordInput(attrs={
        
        'placeholder':'Password',
    }))
    def __init__(self, request=None, *args, **kwargs):
        super(lessorLoginForm, self).__init__(request, *args, **kwargs)



class CustomerProfileEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CustomerProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Enter Phone Number',
            }
        )

    class Meta:
        model = User
        fields = ["first_name", "last_name", 'phone_number',"gender"]
