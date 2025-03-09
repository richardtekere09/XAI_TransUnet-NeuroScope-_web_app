from django import forms
from django.contrib.auth.models import User

class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)  # Optional Profile Picture

    class Meta:
        model = User
        fields = ['username', 'email']
