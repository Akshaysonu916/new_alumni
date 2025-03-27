from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    is_alumni = forms.BooleanField(required=False, initial=False, label="Are you an Alumni?")
    is_student = forms.BooleanField(required=False, initial=True, label="Are you a Student?")
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_alumni', 'is_student')

class SignInForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['job_name', 'company', 'description', 'job_type', 'application_link', 'company_website']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image']

class AlumniProfileForm(forms.ModelForm):
    class Meta:
        model = AlumniProfile
        fields = ['profile_picture', 'bio', 'company', 'job_title', 'graduation_year', 'linkedin']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a short bio...'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company Name'}),
            'job_title': forms.TextInput(attrs={'placeholder': 'Your Job Title'}),
            'graduation_year': forms.NumberInput(attrs={'placeholder': 'Graduation Year'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'LinkedIn Profile URL'}),
        }