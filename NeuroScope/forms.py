from django import forms
from django.contrib.auth.models import User
from .models import Profile ,MRI_Scan

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)  # Allows uploading a profile picture

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'github', 'linkedin', 'twitter', 'certificate']

class MRIScanForm(forms.ModelForm):
    class Meta:
        model = MRI_Scan
        fields = ['patient_uid', 'notes', 'tags', 'scan_file']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }