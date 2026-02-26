from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Skills, Message


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        labels = {
            "first_name":"Full Name"
        }
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class":"input"})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class":"input"})

class SkillForm(ModelForm):
    class Meta:
        model = Skills
        fields=["name", "description"]
    
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class":"input"})
            
            
class messageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "name", "email", "body"]
    
    def __init__(self, *args, **kwargs):
        super(messageForm, self).__init__(*args, **kwargs)
        
        for _, field in self.fields.items():
            field.widget.attrs.update({"class":"input"})