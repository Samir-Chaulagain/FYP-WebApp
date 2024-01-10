from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from accounts.models import User

class CustomerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=10, required=True, label='Phone Number',
                                   widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}))
    photo = forms.ImageField(label='Upload a Profile', required=False)   
    document_photo = forms.ImageField(label='Upload a Profile', required=False)   
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number',  'password1', 'password2', 'gender', 'photo','document_photo' ]
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
        self.fields['document_photo'].label = "Document_photo:"

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
        


    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = UserCreationForm.save(self,commit=False)
        user.role = "customer"
        if user.document_photo:
            user.is_verified = True
        if commit:
            user.save()
        return user
        
    
class LessorRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=10, required=True, label='Phone Number',
                                   widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}))
    photo = forms.ImageField(label='Upload a Profile', required=False)
    document_photo = forms.ImageField(label='Upload a Profile', required=False)
   
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
        self.fields['photo'].label = "Photo :"
        self.fields['document_photo'].label = "Document_Photo :"
        

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
        fields = ['first_name', 'last_name', 'email', 'phone_number',  'password1', 'password2', 'gender','photo','document_photo']

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = UserCreationForm.save(self,commit=False)
        user.role = "lessor"
        if user.document_photo:
            user.is_verified = True
        if commit:
            user.save()
        return user

class CustomerProfileEditForm(forms.ModelForm):
    

    photo = forms.ImageField(label='Upload a Profile', required=False)
    document_photo = forms.ImageField(label='Upload a document', required=False)
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
        self.fields['photo'].widget.attrs.update({'placeholder': 'Change Profile Picture'}) 

        self.fields['document_photo'].widget.attrs.update({'placeholder': 'Change Document Photo'})
    class Meta:
        model = User
        fields = ["first_name", "last_name", 'phone_number',"gender","photo",'document_photo']

class LessorProfileEditForm(forms.ModelForm):
    photo = forms.ImageField(label='Change Profile Picture')
    document_photo = forms.ImageField(label='Change Profile Picture')
    def __init__(self, *args, **kwargs):

        super(LessorProfileEditForm, self).__init__(*args, **kwargs)
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
        self.fields['photo'].widget.attrs.update({'placeholder': 'Change Profile Picture'})
        self.fields['document_photo'].widget.attrs.update({'placeholder': 'Change Document'})

    class Meta:
        model = User
        fields = ["first_name", "last_name", 'phone_number',"gender",'photo','document_photo']





        

# Custom form for initiating password reset process
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',  # Label for the email field
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your Email', 'autocomplete': 'email'}),
        # Email input field with placeholder and autocomplete attribute
    )

# Customized password reset form, based on Django's BasePasswordResetForm
class PasswordResetForm(BasePasswordResetForm):
    email = forms.EmailField(
        label='Email',  # Label for the email field
        max_length=254,  # Maximum length for the email field
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your Email', 'autocomplete': 'email'}),
        # Email input field with placeholder and autocomplete attribute
    )

# Change Password code 
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password: ",
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    new_password1 = forms.CharField(
        label="New Password: ",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    new_password2 = forms.CharField(
        label="Confirm Password: ",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')

        if old_password:
            user = self.user

            # Check if the old password is correct
            if not user.check_password(old_password):
                self.add_error('old_password', 'The old password is incorrect.')

        return cleaned_data


class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="Enter your new password.",
    )
    
    new_password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The passwords do not match.")

        return cleaned_data
