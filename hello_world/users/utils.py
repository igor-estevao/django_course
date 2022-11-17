from django.db.models import Q # lib to work with custom querys with OR
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Profile, Skills

def pagination_profiles(request, profiles, results_per_page):
# Initializing the paginator
  if request.GET.get("page"):
    page = request.GET.get("page")
    request_copy = request.GET.copy()
    request_copy.pop("page")
    url = request_copy.urlencode()  
  else:
    page = 1
    url = request.get_full_path()

  paginator = Paginator(profiles, results_per_page)
  try:
    profiles = paginator.page(page)
  except PageNotAnInteger:
    page = 1
    profiles = paginator.page(page)
  except EmptyPage:
    page = paginator.num_pages
    profiles = paginator.page(page)

  left_index = int(page) - 4
  right_index = int(page) + 5
  
  if left_index < 1 : left_index = 1
  if right_index > paginator.num_pages : right_index = paginator.num_pages + 1

  custom_range = range(left_index, right_index)

  return profiles, custom_range, url


def search_profiles(request):
  search_query = request.GET.get("q") if request.GET.get("q") else ""

  # Check if there is any skills that the name match the query
  skills = Skills.objects.filter(name__icontains=search_query)

  # The Q helps making a query on filter that accepts an OR condition
  profiles = Profile.objects.distinct().filter(
    Q(name__icontains=search_query) |
    Q(short_intro__icontains=search_query) |
    Q(skills__in=skills) # Testing if the profile has at least a skill listed in the skills query
  )

  return profiles, search_query