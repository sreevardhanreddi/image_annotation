import csv
import json
import os

from django.contrib.auth.decorators import login_required
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
from annotate_app.models import Annotations, Images, ProjectFolder


def index(request):
    return render(request, "index.html", {})


@login_required
def view_all_projects(request):
    projects = ProjectFolder.objects.filter(created_by=request.user)
    return render(request, "projects.html", {"projects": projects})


@login_required
def view_project_images(request, pk):
    project = get_object_or_404(ProjectFolder, pk=pk, created_by=request.user)
    images = Images.objects.filter(project=project)
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


def handle_uploaded_file(f, path):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required
def upload_images(request):
    if request.method == "GET":
        if not os.path.exists("media/images"):
            os.makedirs("media/images")
        return render(request, "upload.html", {})

    if request.method == "POST":
        project_name = request.POST.get("project", None)
        if project_name:
            project_instance = ProjectFolder.objects.filter(name=project_name).first()
            if not project_instance:
                project_instance = ProjectFolder.objects.create(
                    name=project_name, created_by=request.user
                )

            image_files = request.FILES
            total_files = len(request.FILES)
            if total_files:
                for im in range(total_files):
                    path = "media/images/" + project_name + "/"
                    image_file = request.FILES.get("image" + "[" + str(im) + "]", None)
                    if image_file:
                        handle_uploaded_file(image_file, path)
                        image_path = "/images/" + project_name + "/" + image_file.name
                        Images.objects.create(
                            project=project_instance, image=image_path
                        )

                return redirect(reverse("annotate:get_all_images"))
            else:
                return render(request, "upload.html", {})
        else:
            return render(request, "upload.html", {})


@login_required
def get_all_images(request):
    projects = ProjectFolder.objects.filter(created_by=request.user).values_list(
        "id", flat=True
    )
    images = Images.objects.filter(project_id__in=projects)
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


@login_required
def annotate_image(request, pk):
    image = get_object_or_404(Images, pk=pk)

    if request.user != image.project.created_by:
        return HttpResponse(403, status=403)

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


@login_required
def view_annotations(request, pk):
    image = get_object_or_404(Images, pk=pk)
    if request.user != image.project.created_by:
        return HttpResponse(403, status=403)
    data = image.get_annotations
    data = json.dumps(data)
    return render(request, "view_annotations.html", {"image": image, "data": data})


@login_required
def download_image_annotations(request, pk):
    image = get_object_or_404(Images, pk=pk)
    if request.user != image.project.created_by:
        return HttpResponse(403, status=403)
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
