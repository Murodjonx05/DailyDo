from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Work

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email address'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))

class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['name', 'short_name', 'work_type', 'location', 'price_text', 'other_text', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Job Title'}),
            'short_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Short Description'}),
            'work_type': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Location (Optional)'}),
            'price_text': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Budget / Rate'}),
            'other_text': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Additional Details'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select', 'style': 'height: 100px;'}),
        }
