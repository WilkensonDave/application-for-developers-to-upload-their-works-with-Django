from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Project, Tag, Review
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import SearchProjects, paginateProjects
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import re
# Create your views here.


def projects(request):
    search_query, projects = SearchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)
    
    context ={
        "projects":projects,
        "search_query":search_query,
        "custom_range":custom_range
    }
    return render(request, "projectdev/projects.html", context)

def single_project(request, pk):
    
    project = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.user.is_authenticated:
        profile = request.user.profile
        
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            if Review.objects.filter(owner=profile, project=project).exists():
                messages.error(request, "Sorry, you can not submit another review for this project")
                return redirect("single-project", project.id)
            review.project = project
            review.owner = profile
            review.save()
            project.getVoteCount
            messages.info(request, "Review has been successfully added.")
            return redirect("single-project", pk=project.id)
        
        else:
            messages.error(request, "Invalid request")
        
    context = {
        "project":project,
        "form":form
    }
    return render(request, "projectdev/single-project.html", context)

@login_required(login_url="login")
def createProject(request):
    form = ProjectForm
    profile = request.user.profile
    if request.method == "POST":
        new_tags = request.POST.get("newtags")
        project_tags = re.split(r"[,;\s]+", new_tags)
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in project_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                if created:
                    project.tags.add(tag)
            messages.info(request, "Project has been Successfully created.")
            return redirect("account")
        
        else:
            error = {"error":"Invalid form"}
            return render(request, "projectdev/project_form.html",
                          context={"error":error})
    
    return render(request, "projectdev/project_form.html",
                  context={"form":form})


@login_required(login_url="login")
def updateproject(request, pk):
    profile = request.user.profile
    project = profile.projects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        new_tags = request.POST.get("newtags")
        project_tags = re.split(r"[,;\s]+", new_tags)
        
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project_tag = form.save()
            for tag in project_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                if created:
                    project_tag.tags.add(tag)
            messages.info(request, "Project has been successfully deleted.")
            return redirect("account")
    
    context = {
        "form":form,
        "project": project
    }
    return render(request, "projectdev/project_form.html", context)


@login_required(login_url="login")
def deleteproject(request, pk):
    profile = request.user.profile
    project = profile.projects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("projects")
    
    context = {
        "object":project
    }
    return render(request, "delete_template.html", context)