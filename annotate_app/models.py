import json

from django.core import serializers
from django.db import models


class Images(models.Model):
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
