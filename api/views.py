from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializers,ReviewSerializers
from  appfordevelopers.models import Project, Review, Tag


@api_view(["GET"])
def getRoutes(request):
    routes = [
        {"GET":"api/projects"},
        {"GET":"api/projects/id"},
        {"POST":"api/projects/id/vote"},
        {"POST":"api/users/token"},
        {"GET":"api/users/token/refresh"},
    ]
    
    return Response(routes)


@api_view(["GET"])
def get_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializers(projects, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def project(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializers(project, many=False      )
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data
    review, created = Review.objects.get_or_create(owner=user, project=project)
    if created:
        review.value = data['value']
        review.save()
        project.getVoteCount
    serializer = ProjectSerializers(project, many=False)
    return Response(serializer.data)

@api_view(["DELETE"])
def removeTag(request):
    tagId = request.data["tag"]
    projectId = request.data["project"]
    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)
    project.tags.remove(tag)
    return Response("Tag was deleted")