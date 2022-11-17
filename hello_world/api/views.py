from django.http import JsonResponse
from rest_framework.decorators import permission_classes, api_view # decorator do allow specify what CRUD methods the def will be allowing
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import *
from api import serializers

@api_view(["GET"])
def get_routes(request):

  routes = [
    { "GET" : "/api/projects" },
    { "GET" : "/api/projects/id" },
    { "POST" : "/api/projects/id/vote" },
    { "POST" : "/api/projects/id/vote" },

    { "POST" : "/api/users/token" },
    { "POST" : "/api/users/token/refresh" }
  ]

  return Response(routes)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def projects(request):
  projects = Project.objects.all() # Get all project objects
  serializer = ProjectSerializer(projects, many=True) # serialize all of them 
  
  return Response(serializer.data) # serializer.data is just all of the projects data as JSON

@api_view(["GET"])
def project(request, pk):
  projects = Project.objects.get(id=pk) # Get the project
  serializer = ProjectSerializer(projects, many=False) # serialize it
  
  return Response(serializer.data) # serializer.data is just the projects data as JSON

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def review_project(request, pk):
  project = Project.objects.get(id=pk)
  profile = request.user.profile
  data = request.data

  review, created = Review.objects.get_or_create(
    owner = profile,
    project = project,
  )

  review.value = data["value"],
  review.save()
  project.set_vote_count

  print("DATA:", data)
  serializer = ProjectSerializer(project, many=False)

  return Response(serializer.data)