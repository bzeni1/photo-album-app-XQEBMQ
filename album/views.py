from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Photo
from .forms import PhotoUploadForm


def photo_list(request):
    sort = request.GET.get("sort", "date")

    qs = Photo.objects.all()

    if request.user.is_authenticated:
        qs = qs.filter(owner=request.user)
    else:
        qs = qs.none()

    if sort == "name":
        photos = qs.order_by("name", "-uploaded_at")
    else:
        photos = qs.order_by("-uploaded_at", "name")

    return render(request, "album/list.html", {
        "photos": photos,
        "sort": sort,
        "current_sort": sort,
    })


@login_required
def photo_upload(request):
    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data["name"]
            image = form.cleaned_data["image"]

            Photo.objects.create(
                name=name,
                image=image,
                owner=request.user,
            )
            return redirect("photo_list")
    else:
        form = PhotoUploadForm()

    return render(request, "album/upload.html", {"form": form})


def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

    if not request.user.is_authenticated or photo.owner != request.user:
        return HttpResponseForbidden("Nincs jogosultságod megnezni ezt a kepet!")

    return render(request, "album/detail.html", {"photo": photo})


@login_required
def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

    if photo.owner != request.user:
        return HttpResponseForbidden("Nincs jogosultságod torolni ezt a kepet!")

    if request.method == "POST":
        if photo.image:
            photo.image.delete(save=False)
        photo.delete()
        return redirect("photo_list")

    return render(request, "album/delete_confirm.html", {"photo": photo})