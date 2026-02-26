from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="profile")
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(max_length=500, blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    headline = models.CharField(max_length=300, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=300, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profilepictures", null=True, blank=True, default="profilepictures/userdefault.png")
    social_github = models.CharField(max_length=2000, null=True, blank=True)
    social_twitter = models.CharField(max_length=2000, null=True, blank=True)
    social_linkedin = models.CharField(max_length=2000, null=True, blank=True)
    social_youtube = models.CharField(max_length=2000, null=True, blank=True)
    social_website = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.username)
    
    class Meta:
        ordering = ["created", "username"]
    
    @property
    def profileImageUrl(self):
        try:
            url = self.profile_image.url
        except:
            url = ""
        return url

class Skills(models.Model):
    onwer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="skills", null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name)

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ["is_read", "-created"]