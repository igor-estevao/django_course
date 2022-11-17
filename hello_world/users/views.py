from django.core.mail import send_mail # https://docs.djangoproject.com/en/4.1/topics/email/
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm, ProfileForm, SkillsForm, MessageForm
from .models import *
from .utils import search_profiles, pagination_profiles

# TODO: Fix all the routes and method names, using a RoR pattern

def loginUser(request):
  page = "login"
  context = { "page" : page }

  if request.user.is_authenticated:
    # return redirect(request.META.get('HTTP_REFERER'))
    return redirect("profiles")

  if request.method == "POST":
    username = request.POST["username"]
    password = request.POST["password"]

    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request, "Username does not exist")

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      messages.info(request, "User Logged in")

      return redirect(request.GET.get("next") if request.GET.get("next") else "account")


      return redirect("profiles")
    else:
      messages.error(request, "Username or Password incorrect")


  return render(request, "users/login_registration.html", context)

def logoutUser(request):
  logout(request)
  messages.info(request, "User Logged Out")
  return redirect("login")

def registerUser(request):
  page = "register"
  form = CustomUserCreationForm()

  if request.method == "POST":
    print("Here we are with the creation request")
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()

      messages.success(request, "User Account Created Successful!")
      login(request, user)
      return redirect("edit_user_account")

  context = { "page" : page, "form" : form }
  return render(request, "users/login_registration.html", context)

def profiles(request):

  profiles, search_query = search_profiles(request)

  results_per_page = 3

  profiles, custom_range, url = pagination_profiles(request, profiles, results_per_page)

  context = {
    "profiles" : profiles,
    "search_query" : search_query,
    "custom_range" : custom_range,
    "url" : url
  }
  return render(request, "users/profiles.html", context)

def userProfile(request, pk):
  profile = Profile.objects.get(id=pk)
  topSkills = profile.skills_set.exclude(description="")
  otherSkills = profile.skills_set.filter(description="")
  
  context = { 
    "profile" : profile,
    "topSkills" : topSkills,
    "otherSkills" : otherSkills
  }
  
  return render(request, "users/profile.html", context)

@login_required(login_url="login")
def userAccount(request):
  profile = request.user.profile
  skills = profile.skills_set.all()
  projects = profile.project_set.all()
  context = { 
    "profile" : profile,
    "skills" : skills,
    "projects" : projects
    }
  return render(request, "users/account.html", context)

@login_required(login_url="login")
def edit_user_account(request):

  profile = request.user.profile
  form = ProfileForm(instance=profile)
  if request.method == "POST":
    form = ProfileForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
      form.save()
      return redirect("account")

  context = { "form" : form }
  return render(request, "users/profile_form.html", context)

@login_required(login_url="login")
def create_skill(request):

  profile = request.user.profile

  form = SkillsForm()

  if request.method == "POST":
    form = SkillsForm(request.POST)
    if form.is_valid():
      skill = form.save(commit=False)
      skill.owner = profile
      skill.save()
      messages.success(request, "Skill Was Added!")
      return redirect("account")


  context = { "form" : form }
  return render(request, "users/skill_form.html", context)

@login_required(login_url="login")
def edit_skill(request, pk):
  profile = request.user.profile
  skill = profile.skills_set.get(id=pk)
  form = SkillsForm(instance=skill)

  if request.method == "POST":
    form = SkillsForm(request.POST, instance=skill)
    if form.is_valid():
      form.save()
      messages.success(request, "Skill Was Updated!")
      return redirect("account")


  context = { "form" : form }
  return render(request, "users/skill_form.html", context)

@login_required(login_url="login")
def delete_skill(request, pk):
  profile = request.user.profile
  skill = profile.skills_set.get(id=pk)

  if request.method == "POST":
    skill.delete()
    messages.success(request, "Skill was successfully deleted!")
    return redirect("account")

  context = { "object" : skill }
  return render(request, "delete_confirmation.html", context)

@login_required(login_url="login")
def inbox(request):
  profile = request.user.profile
  chat_messages = profile.messages.all() # since I set related_name, we call ".messages" instead of message_set
  unread_count = chat_messages.filter(is_read=False).count
  
  context = {
    "chat_messages" : chat_messages,
    "unread_count" : unread_count
   }
  return render(request, "users/inbox.html", context)

@login_required(login_url="login")
def message(request, pk):
  message = request.user.profile.messages.get(id=pk)
  
  # Since got here, we must set the is_read property to True
  message.is_read = True
  message.save()

  context = {
    "message" : message,
  }
  return render(request, "users/message.html", context)


# I will allow not logged users to send message to a profile. 
def send_message(request, pk):
  recipient = Profile.objects.get(id=pk)
  sender = None
  
  form = MessageForm()

  if request.user.is_authenticated:
    sender = Profile.objects.get(id=request.user.profile.id)
  if request.method == "POST":
    form = MessageForm(request.POST)
    if form.is_valid():
      message = form.save(commit=False)
      message.sender = sender
      message.recipient = recipient

      if sender:
        message.name = sender.name
        message.email = sender.email

      message.save()

      messages.success(request, "Your message was successfully sent to", recipient)
      return redirect("profile", pk=recipient.id)


  context = {
    "form" : form,
    "recipient" : recipient
  }
  return render(request, "users/message_form.html", context)
