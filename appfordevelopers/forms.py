from django.forms import ModelForm
from django import forms
from .models  import Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude=["profile", "id", "vote_ratio", 
                 "vote_total", "owner", "tags"]
        
        
        widgets = {
            "tags":forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class":"input"})
        # self.fields["title"].widget.attrs.update({"class":"input", 'placeholder':"Add Title"})
        # self.fields["description"].widget.attrs.update({"class":"input", 'placeholder':"Add Description"})

class ReviewForm(ModelForm):
    
    class Meta:
        model=Review
        fields = ["value", "description"]

        labels ={
            'value':"Place your Vote",
            "description": "Add a description with your vote."
        }
        
        widgets = {
            "description":forms.Textarea(
                attrs={
                    "placeholder":"Enter your description here."
                }
            )
        }
        
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({"class":"input"})