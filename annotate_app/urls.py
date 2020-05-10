from django.urls import path

from annotate_app.views import (
    annotate_image,
    download_image_annotations,
    get_all_images,
    index,
    upload_images,
    view_annotations,
)

app_name = "annotate"

urlpatterns = [
    path("", index, name="index"),
    path("upload-images/", upload_images, name="upload_images"),
    path("all-images/", get_all_images, name="get_all_images"),
    path("annotate-images/<int:pk>/", annotate_image, name="annotate_image"),
    path("view-images/<int:pk>/", view_annotations, name="view_annotations"),
    path(
        "download-image-annotations/<int:pk>/",
        download_image_annotations,
        name="download_image_annotations",
    ),
]
