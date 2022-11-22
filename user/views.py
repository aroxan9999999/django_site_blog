from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from .forms import Userloginform, Userregistrationform, Userupdateform
from django.contrib import messages

User = get_user_model()

def login_view(request):
    form = Userloginform(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("post_list")
    return render(request, "login.html", context={"form": form})


def logout_view(request):
    logout(request)
    return redirect("post_list")

def register_view(request):
    form = Userregistrationform(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data["password"])
        new_user.save()
        messages.success(request, 'Account created successfully.')
        return redirect("post_list")
    return render(request, "register.html", context={"form": form})

def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        form = Userupdateform(initial={"username": user.username,
                                        "first_name": user.first_name, "last_name": user.last_name})
        if request.method == "POST":
            form = Userupdateform(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                username = data["name"]
                if User.objects.filter(username=username):
                    pass
                else:
                    user.username = username
                user.firstname = data["name"]
                user.set_password(data["password"])
                user.save()
                user = authenticate(username=username, password=data["password"])
                login(request, user)
                messages.success(request, 'данные успешно обнавлены')
                return redirect("post_list")
        return render(request, "update.html", context={"form": form})

def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        _us = User.objects.get(pk=user.pk)
        _us.delete()
        messages.error(request, 'Акаунт удален.')
    return redirect("register")