#forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Product, UserAddress,SellerProfile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'image']


class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = [
                  'state',
                  'city',
                  'pincode',
                  ]

class SellerProfileForm(forms.ModelForm):
    
    class Meta:
        model = SellerProfile
        fields = ['mobile', 
                  'address', 
                  'profile_picture', 
                  'bio','joined_on',
                  'adhaar_number',
                  'account_number',
                  'ifsc_code',
                  ]
        
class PasswordResetForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
        
