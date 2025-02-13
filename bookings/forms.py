from django import forms
from .models import Booking, User
from django.contrib.auth.models import User



class UserCreationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'table', 'date_time', 'number_of_guests']
    
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class AuthenticateForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)    