# Django-Course
This is the rep for all Projects from [Python Django - Complete Course
](https://www.udemy.com/course/python-django-2021-complete-course/)

I won`t be separating a single rep for every app, only if it is
necessary and interesting for me :)

---
## Basic Setups Projects
Having Django installed:


-To create a project, run:

```django-admin startproject <project_name>```

-Change directory to the project, and create a virtual enviroment(I`m seting name as "env"): 

```virtualenv env```

-And then, to activate the virtual enviroment:

```env/bin/activate```

-On MacOSX, make sure to write ```source```

```source env/bin/activate```

-To deactivate the venv. (Not working for some reason, I`m just exiting the terminal): 

```env/bin/deactivate```

---
## Apps inside Projects

-Inside the project directory, when we want to add a new featur for the project, for some cases, we must create a separate app.
To make a new app, we must run:

```python manage.py startapp <app_name>```

(or python3, my case)

---
## Starting Server

-To start the server, we run the manage.py file as:

```python manage.py runserver```

-Then we go to [Localhost](http://localhost:8000) to see the Index page.

---
## Admin Panel

-For start working with Models, we must run a migration, to setup the database file(on this case, sqlite):

```python manage.py migrate```

This command will create a migration and a [Admin Page](http://localhost:8000/admin)

-To access this Admin Page, we must create a super user:

```python manage.py createsuperuser```

-Then proceed to create your user, with super user access and you will be able to access the Admin Panel, where you can make all CRUD operations on the go.

## Models

-For creating a table in the database, we need to create a class in the models.py file, inside the app folder

```python:
## ./main/models.py

from django.db import models
import uuid
# Create your models here.
class Project(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True)
  demo_link = models.CharField(max_length=2000, null=True, blank=True)
  source_link = models.CharField(max_length=2000, null=True, blank=True)
  created = models.DateTimeField(auto_now_add=True) #timestamps just like Rails
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
```

-And then, we are able to run our migration, to prepare the database to create the Project Table.

-To create the schema file, we must run:

```python manage.py makemigrations```

-Then, with the schema file created, we run the code to create the table:

```python manage.py migrate```

-With the table created, we must register the model into the Admin Panel. We do that by adding this code to the admin.py inside the app

```python:
#./main/admin.py
from django.contrib import admin

# Register your models here.
from .models import Project

admin.site.register(Project)
```

-That beeing done, we are able to access this table on the Admin Panel and play with the Project table.

---
## Database Relations

-To create a One to Many database relation, we must create add a ForeignKey into the new class, on the models.py. That being said, it was added the Review class into the file, and this is the code:

```python:

#./main/models.py

class Review(models.Model):
  # owner = 
  project = models.foreignKey(Project, on_delete=models.CASCATE) # linking the project_id into the review

  VOTE_OPTIONS = (
    ("up", "Up Vote"),
    ("down", "Down Vote")
  )# Similar to enum, on rails

  body = models.TextField(null=True, blank=True)
  value = models.CharField(max_length=200, choices=VOTE_OPTIONS)
  created = models.DateTimeField(auto_now_add=True) #timestamps just like Rails
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
```

-And to work with Many to Many Relations, a Tag class was added, and with it, was added the line:  ```tag = models.ManyToManyField("Tag", blank=True)``` to the Project class. 

-Tag class: 

```python:
#./main/models.py
class Tag(models.Model):
  name = models.CharField(max_length=200)
  created = models.DateTimeField(auto_now_add=True) #timestamps just like Rails
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

  def __str__(self):
    return self.value
```

-For custom use, it was added to the Project class:

```python: 
vote_total = models.IntegerField(default=0, null=True, blank=True)
vote_ratio = models.IntegerField(default=0, null=True, blank=True)
```

-After that, just run ```python manage.py makemigrations``` and then: ```python manage.py migrate``` to do the trick.
-Then just add this two new models into the Admin Panel

```python:
#./main/admin.py
from django.contrib import admin

# Register your models here.
from .models import Project, Review, Tag

admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)
```

-Nice, now we have the Models and some basic relations to work with in the Admin Panel

---

## Queries

-Queries in Django are very simple, as an example:

```python:
#listing all objects of this Model on the Database(and others)
  queryset = ModelName.objects.all()
                              .get()
                              .filter()
                              .exclude()

#filter use
  queryset = ModelName.objects.filter(attribute="value")
                              .filter(attribute__startswith="value")
                              .filter(attribute__contains="value")
                              .filter(attribute__icontains="value")
```
### Testing Queries


-One way to check for data and test query and commands, we can run an Django CLI. To open an Django console, we must run:

```python manage.py shell```

-Running the shell, to access an model, we must import it to be visible in the context(for example, showing the Project model):

```from main.models import Project````

-To get all Projects, we can run as:

```projects = Project.objects.all()````

-To get with some where conditions, we can run as:
```projectObj = Project.objects.get(title="Project Testing")```

-Then print them all:

```print(projects)```

-And to print single with attribute

```print(projectObj.title)```

-Let`s filter:

```projects = Project.objects.filter(title__startswith="Pro")```

-Filtering Numbers, testing number Greater then and equals:

```projects = Project.objects.filter(vote_ratio__gte=50)```

-Basically, 'filter' sends a "where" with some condition, and 'excludes' is just "where not".

-We can access the children of some model by calling it as this:

```project.review_set.all()```

-This returns all the children Reviews that has the defined Project(stored at project variable), as its parent.

### Conclusions

-From now on, I\`ll be just commenting on the code :) Writing this is cool but if it\`s already commented, it`s documented.