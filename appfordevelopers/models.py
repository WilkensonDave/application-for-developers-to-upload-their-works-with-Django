from django.db import models
import uuid
from django.contrib.auth.models import User
from users.models import Profile
from django.core.exceptions import ValidationError
# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="projects", null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name="projects")
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    featured_image = models.ImageField(upload_to="featured-images", null=True, blank=True,
            default="featured-images/default.jpg")
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-vote_ratio", '-vote_total', "-created", "title"]
    
    @property
    def imageUrl(self):
        try:
            url = self.featured_image.url
        except:
            url = ""
            
        return url
        
    @property
    def getVoteCount(self):
        reviews = self.reviews.all()
        upVotes = reviews.filter(value="up").count()
        totalVotes = reviews.count()
        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()
    
    #if the login users already submit a review for a project they will not see the review form
    #it will display another message telling the user they have already reviewed the project
    @property
    def reviewers(self):
        queryset = self.reviews.all().values_list("owner__id", flat=True)
        return queryset

class Review(models.Model):
    VOTE_TYPE = (
        ("up", "Up Vote"),
        ("down", "Down Vote")
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="review")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="reviews")
    description = models.TextField(max_length=300, null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.value
    
    class Meta:
        unique_together =[['owner', 'project']]
    
    #this is to prevent prople from voting their own project
    def clean(self):
        if self.owner and self.project  == self.project.owner:
            raise ValidationError("You can not review your own project.")


class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

