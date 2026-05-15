from django.contrib.auth import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django import forms
from django.forms import widgets
from .models import AdminProfile, SellerProfile, Subcategory

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control', 'placeholder':'Username'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control', 'placeholder':'Password'}),
    )


class SellerSignupForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    shopname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shop Name'}))
    gstno = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'GST Number', 'onchange':'validate_gst()'}))
    pswd = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    cpswd = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))
        

class CustomerSignupForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    pswd = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    cpswd = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))


class AddSubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['category', 'subcategory']
        widgets = {
            'category':forms.Select(attrs={'class':'form-control'}),
            'subcategory':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Subcategory Name'})
        }
        

        

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = ['contact_number', 'city', 'state', 'zipcode', 'image']
        widgets = {
            'contact_number':forms.NumberInput(attrs={'class':'form-control','placeholder':'Contact Number'}),
            'city':forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}),
            'state':forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}),
            'image':forms.FileInput(attrs={'class':'btn btn-primary d-none', 'id':'admin_image_upload', 'onchange':'showPreview(event)'}),
        }


class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['contact_number', 'shop_name', 'shop_address', 'gst_number', 'image']
        widgets = {
            'contact_number':forms.NumberInput(attrs={'class':'form-control','placeholder':'Contact Number'}),
            'shop_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shop Name'}),
            'shop_address':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Shop Address', 'rows':5}),
            'gst_number':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'GST Number'}),
            'image':forms.FileInput(attrs={'class':'btn btn-primary d-none', 'id':'admin_image_upload', 'onchange':'showPreview(event)'}),
        }


class AdminSellerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
        }
    

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'current-password', 'autofocus': True,}),
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password'}),
    )
