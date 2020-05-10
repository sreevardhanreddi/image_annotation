import csv
import json
import os

from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import (
    HttpResponse,
    HttpResponseRedirect,
    get_object_or_404,
    redirect,
    render,
    reverse,
)

from annotate_app.forms import ImageUploadForm
from annotate_app.models import Annotations, Images


def index(request):
    return render(request, "index.html", {})


def check_folder(request):
    folder_name = request.GET.get("folder_name", "")
    data = os.path.isdir("media/images/{}".format(folder_name)) and os.path.exists(
        "media/images/{}".format(folder_name)
    )
    return JsonResponse({"data": data})


def upload_images(request):
    if request.method == "GET":
        return render(request, "upload.html", {})

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        return redirect(reverse("annotate:get_all_images"))


def get_all_images(request):
    images = Images.objects.filter()
    annotated_images = Annotations.objects.values_list("image_id", flat=True)
    annotated_images = images.filter(id__in=annotated_images)
    non_annotated_images = images.exclude(id__in=annotated_images)

    return render(
        request,
        "images_list.html",
        {
            "annotated_images": annotated_images,
            "non_annotated_images": non_annotated_images,
        },
    )


def annotate_image(request, pk):
    image = get_object_or_404(Images, pk=pk)

    if request.method == "POST":
        annotations = request.POST.get("annotations", None)
        if annotations:
            annotations = json.loads(annotations)
            for annotation in annotations:
                annotation_obj = Annotations(**annotation)
                annotation_obj.image = image
                annotation_obj.save()

            return redirect(reverse("annotate:get_all_images"))
        else:
            return render(
                request,
                "annotate_image.html",
                {"image": image, "errors": "Please annotate the image"},
            )

    return render(request, "annotate_image.html", {"image": image})


def view_annotations(request, pk):
    image = get_object_or_404(Images, pk=pk)
    data = image.get_annotations
    data = json.dumps(data)
    return render(request, "view_annotations.html", {"image": image, "data": data})


def download_image_annotations(request, pk):
    image = get_object_or_404(Images, pk=pk)
    data = image.get_annotations
    csv_list = []
    file_name = image.image.name.strip("images/")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename={}.csv".format(file_name)
    for el in data:
        temp = [
            file_name,
            el["left"],
            el["top"],
            el["width"],
            el["height"],
            el["label"],
        ]
        csv_list.append(temp)

    writer = csv.writer(response)
    writer.writerows(csv_list)
    return response
