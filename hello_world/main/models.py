from django.db import models
import uuid
from users.models import Profile

class Project(models.Model):
  owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True)
  featured_image = models.ImageField(null=True, blank=True, upload_to="projects/", default="projects/default.jpg") # changed this so the projects image will be picked exclusively on the projects folder inside the user_submited_images
  demo_link = models.CharField(max_length=2000, null=True, blank=True)
  source_link = models.CharField(max_length=2000, null=True, blank=True)
  vote_total = models.IntegerField(default=0, null=True, blank=True)
  vote_ratio = models.IntegerField(default=0, null=True, blank=True)
  tag = models.ManyToManyField("Tag", blank=True) # adding with quotes because of lazy loading

  created = models.DateTimeField(auto_now_add=True) #timestamps just like Rails
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

  def __str__(self):
    return self.title # This way, when we are accessing the object, it will show the title whe we print the entire class, instead of a random hash

  @property
  def set_vote_count(self):
    reviews = self.review_set.all()
    up_votes = reviews.filter(value="('up',)").count() # glitch
    total_votes = reviews.count()

    print("Total: ", total_votes)
    print("Upvotes", up_votes)
    if up_votes == 0:
      ratio = 0
    else:
      ratio = (total_votes / up_votes) * 100

    self.vote_total = total_votes
    self.vote_ratio = ratio
    self.save()

  @property
  def image_url(self):
    try:
      url = self.featured_image.url
    except:
      url = "/"
    return url

  class Meta:
    # ordering = [ "-created" ] # Orders by the created field. The - sign indicates desc(last created)
    ordering = [ "-vote_ratio", "-vote_total", "title" ]

  @property
  def reviewers(self):
    return self.review_set.all().values_list("owner__id", flat=True)


class Review(models.Model):
  owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
  project = models.ForeignKey(Project, on_delete=models.CASCADE) # linking the project_id into the review

  VOTE_OPTIONS = (
    ("up", "Up Vote"),
    ("down", "Down Vote")
  )# Similar to enum, on rails

  body = models.TextField(null=True, blank=True)
  value = models.CharField(max_length=200, choices=VOTE_OPTIONS)
  created = models.DateTimeField(auto_now_add=True) #timestamps just like Rails
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

  # Ensuring a review is unique to owner and project: One profile can only have a single review for each project. The inverse is true.
  class Meta:
    unique_together = [["owner", "project"]]

  def __str__(self):
    return (self.project.title + " - " + self.owner.username)

class Tag(models.Model):
  name = models.CharField(max_length=200)
  created = models.DateTimeField(auto_now_add=True) #timestamps just like Rails
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

  def __str__(self):
    return self.name