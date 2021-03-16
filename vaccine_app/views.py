from django.shortcuts import render,redirect
from django.http import HttpResponse
# from django.contrib.auth.models import  User,auth
from .models import VaccineLot, DistrictAdmin, DistrictVaccineData, CenterAdmin, CenterVaccineData, CenterRegestration, Receiver, ReceiverVaccination
from datetime import datetime
from .models import User
from .forms import RegistrationForm

# Create your views here.
def index(request):
    return render(request,"index.html")


def register_user(request):
    if request.user.is_authenticated:
        return render(request,"loggedin.html")

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        print("INside post")
        if registerForm.is_valid():
            print("Inside form")
            # user = registerForm.save(commit=False)
            user=User.objects.create(email=registerForm.cleaned_data["email"])
            user.aadharNumber=registerForm.cleaned_data["aadharNumber"]
            user.first_name=registerForm.cleaned_data["first_name"]
            user.last_name=registerForm.cleaned_data["last_name"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = True
            user.save()
            return render(request, "loggedin.html")
    else:
        registerForm = RegistrationForm()
    return render(request, "register.html", {"form": registerForm})