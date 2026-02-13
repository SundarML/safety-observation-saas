# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email','is_observer','is_action_owner','is_safety_manager')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email','is_observer','is_action_owner','is_safety_manager')
