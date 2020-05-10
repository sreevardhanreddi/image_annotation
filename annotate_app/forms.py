from django import forms

from annotate_app.models import Annotations, Images


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = [
            "image",
        ]
