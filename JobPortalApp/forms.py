from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from JobPortalApp.models import *

class RegisterForm(UserCreationForm):
  class Meta:
    model = CustomUserModel
    fields = ['username','display_name', 'email','user_type', 'password1','password2']

class LoginForm(AuthenticationForm):
  pass

class RecruiterProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = RecruiterProfileModel
    fields = '__all__'
    exclude = ['recruiter']

class SeekerProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = SeekerProfileModel
    fields = '__all__'
    exclude = ['seeker']

class JobPostForm(forms.ModelForm):
  class Meta:
    model = JobPostModel
    fields = '__all__'
    exclude = ['posted_by']

    widgets = {
        'deadline': forms.DateInput(attrs={
            'type': 'date'
        })
    }

class ApplyJobForm(forms.ModelForm):
  class Meta:
    model = ApplyJobModel
    fields = ['resume']
