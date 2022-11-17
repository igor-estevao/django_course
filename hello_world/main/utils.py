from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q # lib to work with custom querys with OR
from .models import Project, Tag


# Pages that has pagination, will return a url without the page param
def pagination_projects(request, projects, results_per_page):
  # Initializing the paginator
  if request.GET.get("page"):
    page = request.GET.get("page")
    request_copy = request.GET.copy()
    request_copy.pop("page")
    url = request_copy.urlencode()
  else:
    page = 1
    url = request.get_full_path()

  if "?" not in url:
    url += "?"
  
  paginator = Paginator(projects, results_per_page)
  try:
    projects = paginator.page(page)
  except PageNotAnInteger:
    page = 1
    projects = paginator.page(page)
  except EmptyPage:
    page = paginator.num_pages
    projects = paginator.page(page)

  left_index = int(page) - 4
  right_index = int(page) + 5
  
  if left_index < 1 : left_index = 1
  if right_index > paginator.num_pages : right_index = paginator.num_pages + 1

  custom_range = range(left_index, right_index)

  return projects, custom_range, url

def search_projects(request):
  search_query = request.GET.get("q") if request.GET.get("q") else ""

  # Check if there is any skills that the name match the query
  tags = Tag.objects.filter(name__icontains=search_query)

  # The Q helps making a query on filter that accepts an OR condition
  projects = Project.objects.distinct().filter(
    Q(title__icontains=search_query) |
    Q(description__icontains=search_query) |
    Q(owner__name__icontains=search_query) |
    Q(tag__in=tags)
  )

  return projects, search_query

# @register.simple_tag(takes_context=True)
# def set_page_param(request, page):
#     query = request.GET.copy()
#     query["page"] = page
#     return query.urlencode()