import json

from django.core import serializers
from django.db import models
from user_auth.models import User


class ProjectFolder(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def get_images_count(self):
        return self.images_set.count()


class Images(models.Model):
    project = models.ForeignKey(ProjectFolder, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_annotations(self):
        annotations = self.annotations_set.all()
        json_data = serializers.serialize(
            "json", annotations, fields=("left", "top", "width", "height", "label")
        )
        data = json.loads(json_data)
        data = [i["fields"] for i in data]
        return data


class Annotations(models.Model):
    image = models.ForeignKey(Images, on_delete=models.CASCADE)
    left = models.IntegerField(default=0)
    top = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    label = models.CharField(max_length=30, default="")
