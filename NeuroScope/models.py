from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to User model
    bio = models.CharField(max_length=200, blank=True, null=True)  # Reduced input size
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Admin verification
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/avatar.png')

    def __str__(self):
        return self.user.username
