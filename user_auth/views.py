
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest
from django.shortcuts import (
    HttpResponse,
    HttpResponseRedirect,
    get_object_or_404,
    redirect,
    render,
    reverse,
)

from user_auth.forms import UserLoginForm, UserSignUpForm
from user_auth.models import User


def user_register(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "GET":
        return render(request, "register.html", {})

    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                email=form.cleaned_data.get("email"),
                username=form.cleaned_data.get("email"),
            )
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("annotate:get_all_images",))
        else:
            return render(request, "register.html", {"errors": form.errors})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "GET":
        return render(request, "login.html", {})

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password,)
            if user is None:
                return render(
                    request,
                    "login.html",
                    {"errors": {"account_error": ["Invalid email or password"]}},
                )

            else:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("annotate:get_all_images",))

                else:
                    return HttpResponse(
                        "# your account is inactive contact admin for details user@example.com"
                    )

        else:
            return render(request, "login.html", {"errors": form.errors})


@login_required(login_url="/login/")
def user_profile(request):
    return render(
        request,
        "profile.html",
        {
        },
    )


def user_logout(request):
    logout(request)
    return redirect(reverse("annotate:index"))
