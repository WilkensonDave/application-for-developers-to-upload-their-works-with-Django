from django.shortcuts import render, redirect
from .models import Profile, Skills, Message
from appfordevelopers.models import Project
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, messageForm
from django.db.models import Q
from .utils import searchProfiles, paginateProfiles
# Create your views here.

def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    
    context ={
        "profiles":profiles,
        "search_query":search_query,
        "custom_range":custom_range
    }
    
    return render(request, "users/profiles.html", context)


def userprofile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skills.exclude(description__exact="")
    otherSkills = profile.skills.filter(description="")
    context = {
        "profile":profile,
        "topSkills":topSkills,
        "otherSkills":otherSkills
    }
    return render(request, "users/user-profile.html", context)

@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    projects = profile.projects.all()
    topSkills = profile.skills.all()
    context={
        "projects":projects,
        "profile":profile,
        "topSkills":topSkills,
    }
    return render(request, "users/account.html", context)


def loginPage(request):
    
    if  request.user.is_authenticated:
        return redirect("profiles")
    
    if request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(username=username)
            
        except:
            messages.error(request, "User does not exist.")
        
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            messages.info(request, "You have been successfully login.")
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        messages.error(request, "Wrong credentials.")
        
    return render(request, "users/login_register.html")

def logoutUser(request):
    logout(request)
    messages.info(request, "You have been successfully logout.")
    return redirect("login")

def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.usename = user.username.lower()
            user.save()
            messages.info(request, "You have been successfully registered. Now Update you personal information to continue.")
            login(request, user)
            return redirect("editaccount")

        else:
            messages.error(request, "Unable to register user. Try Again")
            
    context = {"page":page, "form":form}
    return render(request, "users/login_register.html", context)

login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, "Your profile has been successfully updated.")
            return redirect("account")
    context={
        "profile":profile,
        "form":form
    }
    return render(request, "users/profile_form.html", context)

@login_required(login_url="login")
def createSkills(request):
    form = SkillForm()
    profile = request.user.profile
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.onwer = profile
            skill.save()
            messages.info(request, "Skill has been successfully created.")
            return redirect("account")
        
        else:
            error = {"error":"Invalid form"}
            context = {"error":error}
            return render(request, "users/skill_form.html", context)
        
    context ={
        "form":form
    }
    return render(request, "users/skill_form.html", context)

@login_required(login_url="login")
def delete_skills(request, pk):
    profile = request.user.profile
    skill = profile.skills.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.info(request, "Skill has been successfully deleted.")
        return redirect("account")

    context = {"object":skill}
    return render(request, "delete_template.html", context)


@login_required(login_url="login")
def updateSkills(request, pk):
    profile = request.user.profile
    skill = profile.skills.get(id=pk)
    form = SkillForm(instance=skill)
    
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.info(request, "Skill has been successfully updated.")
            return redirect("account")
        
        else:
            messages.error(request, "Invalid data. Try again")
            return redirect("updateskill")
        
    context = {
        "form":form
    }
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def inbox(request):
    if request.user.is_authenticated:
        profile = request.user.profile
    
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {"messageRequests":messageRequests, "unreadCount":unreadCount}
    return render(request, "users/inbox.html", context)

@login_required(login_url="login")
def viewMessage(request, pk):

    if request.user.is_authenticated:
        profile = request.user.profile
    requestmessage = profile.messages.get(id=pk)
    if requestmessage.is_read == False:
        requestmessage.is_read = True
        requestmessage.save()
    context={
        "message":requestmessage
    }
    return render(request, "users/message.html", context)


def sendMessage(request, pk):
    form = messageForm()
    recipient = Profile.objects.get(id=pk)
    try:
        sender = request.user.profile
        
    except:
        sender = None
    
    if request.method == "POST":
        form = messageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.recipient = recipient
            message.sender = sender
            
            if sender:
                message.name = sender.username
                message.email = sender.email
            message.save()
            
            messages.info(request, "Message  has been successfully sent.")
            return redirect("userprofile", pk=recipient.id)
        
    context = {"recipient":recipient, "form":form}
    return render(request, "users/message_form.html", context)