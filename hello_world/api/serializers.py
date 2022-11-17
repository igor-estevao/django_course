# File responsable for serializing the models data
from rest_framework import serializers
from main.models import *
from users.models import *

# users.models
class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = "__all__"

# main.models 

class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields = "__all__"

class ProjectSerializer(serializers.ModelSerializer):
  owner = ProfileSerializer(many=False)
  tag = TagSerializer(many=True)
  reviews = serializers.SerializerMethodField() # Part 1: allowing the class to return a serialized object on this field (N:1 in this case)
  class Meta:
    model = Project
    fields = "__all__"

  # Part 2: this mess is returning the serialized reviews data
  def get_reviews(self, object):
    reviews = object.review_set.all()
    serializer = ReviewSerializer(reviews, many=True)
    return serializer.data
