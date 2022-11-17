from django.forms import ModelForm
from django import forms
from .models import Project, Review, Tag
# class ProjectForm(forms.Form):
#   title = forms.CharField(max_length=200)

class ProjectForm(ModelForm):
  class Meta:
    model = Project
    fields = ["title", "description", "featured_image" ,"demo_link", "source_link", "tag" ]
        
    widgets = {
      "tag": forms.CheckboxSelectMultiple(),
    }
  
  # Below is some customization of the form

  # Makes no sense doing this but... customizing forms this way is pretty scary and manual.
  # That`s the downside of using this kind of ModelForm or django Forms.
  def __init__(self, *args, **kwargs):
    super(ProjectForm, self).__init__(*args, **kwargs)

    for name, field in self.fields.items():
      field.widget.attrs.update({"class":"input"})

    self.fields["title"].widget.attrs.update({
      "placeholder": "Insert Text Here",
      })

    # self.fields["description"].widget.attrs.update({
    # "class": "input"
    # })

class ReviewForm(ModelForm):
  class Meta:
    model = Review
    fields = [ "value", "body" ]

    labels = {
      "value" : "Place Your Vote",
      "body" : "Add your comment"
    }

  def __init__(self, *args, **kwargs):
    super(ReviewForm, self).__init__(*args, **kwargs)

    for name, field in self.fields.items():
      field.widget.attrs.update({"class":"input"})

    self.fields["body"].widget.attrs.update({
      "placeholder": "Your comment here",
      })
  