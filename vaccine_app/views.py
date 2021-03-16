from django.shortcuts import render,redirect
from django.http import HttpResponse
# from django.contrib.auth.models import  User,auth
from .models import VaccineLot, DistrictAdmin, DistrictVaccineData, CenterAdmin, CenterVaccineData, CenterRegestration, Receiver, ReceiverVaccination, AccessControlList
from datetime import datetime
from .models import User
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout, models

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


def register_admin(request):
    if request.user.is_authenticated:
        return redirect('provide_access')

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
            return redirect('provide_access')
    else:
        registerForm = RegistrationForm()
    return render(request, "register.html", {"form": registerForm})

def provide_access(request):
    pass


def login_gen(request):
    if request.user.is_authenticated:
        return redirect('loggedin')
    err=""
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email = username, password = password)
        if user is not None:
            models.auth.login(request, user)
            return redirect('loggedin')
        else:
           err = 'Input correct email and password'
    template_name = 'login.html'
    context={'err':err}
    return render(request, template_name,context)

def login_center(request):
    if request.user.is_authenticated:
        return redirect('loggedin')
    err=""
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        center = request.POST.get('center')
        user = authenticate(request, email = username, password = password)

        #TODO add_drop_down and center selection

        if user is not None:
            centerAdmin=CenterAdmin.objects.filter(name=center)
            if AccessControlList.objects.filter(person=user,CenterID=centerAdmin).exists() and user.is_centeradmin:
                models.auth.login(request, user)
                return redirect('loggedin')
            else:
                err = 'Access Not allowed'
        else:
           err = 'Input correct email and password'
    
    template_name = 'login_center.html'
    context={'err':err}
    return render(request, template_name,context)







def loggedin(request):
    return render(request,"loggedin.html")
