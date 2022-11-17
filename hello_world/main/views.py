from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q # lib to work with custom querys with OR
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag, Review
from .forms import ProjectForm, ReviewForm
from .utils import search_projects, pagination_projects

def home(request):
  return HttpResponse("Hello World")

def about(request):
  return HttpResponse("This is a about page!")

def param(request, query):
  return HttpResponse("This is a page that has a param: " + str(query))

def projects(request):

  projects, search_query = search_projects(request)

  results_per_page = 3

  projects, custom_range, url = pagination_projects(request, projects, results_per_page)

  context = {
    "projects" : projects,
    "search_query" : search_query,
    "custom_range" : custom_range,
    "url" : url
  }

  return render(request, "main/projects.html", context )

def project(request, pk):
    
  
  project = Project.objects.get(id=pk)
  reviews = project.review_set.exclude(
    Q(body="") #|
    # Q(owner__id=request.user.profile.id)
  )
  reviewers = project.reviewers
  form = ReviewForm()

  if request.method == "POST" and request.user.is_authenticated:
    form = ReviewForm(request.POST)
    review = form.save(commit=False)
    review.project = project
    review.owner = request.user.profile
    review.save()

    project.set_vote_count # Updates the count ratio

    messages.success(request, "Your review was successfully submited!")

    return redirect("project", pk=project.id )

  context = {
    "project" : project,
    "reviews" : reviews,
    "reviewers" : reviewers,
    "form" : form
  }
  return render(request, "main/project.html", context)



@login_required(login_url="login")
def create_project(request):
  profile = request.user.profile
  form = ProjectForm()
  if request.method == "POST":
    form = ProjectForm(request.POST, request.FILES)#Why creating and saving the form when you could save the model🤔?
    if form.is_valid():
      project = form.save(commit=False)
      project.owner = profile
      project.save()
      return redirect("projects")

  context = { "form" : form }
  return render(request, "main/project_form.html", context)

@login_required(login_url="login")
def updade_project(request, pk):
  profile = request.user.profile # The only line of security is here :) 
  project = profile.project_set.get(id=pk)
  form = ProjectForm(instance=project) # Why? 
  if request.method == "POST":
    form = ProjectForm(request.POST, request.FILES, instance=project)
    if form.is_valid():
      form.save()
      return redirect("projects")

  context = { "form" : form }
  return render(request, "main/project_form.html", context)

@login_required(login_url="login")
def delete_project(request, pk):
  profile = request.user.profile # The only line of security is here :) 
  project = profile.project_set.get(id=pk)
  if request.method == "POST":
    project.delete()
    return redirect("projects")
  context = { "object": project }

  return render(request, "delete_confirmation.html", context)

@login_required(login_url="url")
def create_review(request, project_id):
  profile = request.user.profile
  project = Project.objects.get(id=pk)
  form = ModelForm(request.POST)
  form.owner = profile
  form.project = project
  if form.is_valid():
    form.save()
  
  return redirect("project", project.id)

@login_required(login_url="url")
def update_review(request, pk):
  profile = request.user.profile # The only line of security is here :) 
  review = Review.objects.get(id=pk)
  form = ReviewForm(instance=review) # Why? 
  if request.method == "POST":
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
      form.save()

  return redirect("project", review.project.id)