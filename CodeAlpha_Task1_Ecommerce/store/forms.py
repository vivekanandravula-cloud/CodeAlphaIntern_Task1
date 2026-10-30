from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={"placeholder": "Full name"}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"placeholder": "Phone number"}))
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Delivery address"}))
