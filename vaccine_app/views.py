from django.shortcuts import render,redirect
from django.http import HttpResponse
# from django.contrib.auth.models import  User,auth
from .models import VaccineLot, DistrictAdmin, DistrictVaccineData, CenterAdmin, CenterVaccineData, CenterRegestration, Receiver, ReceiverVaccination, AccessControlListCenter,AccessControlListDistrict
from datetime import datetime
from .models import User
from .forms import RegistrationForm, ProvideAccessForm
from django.contrib.auth import authenticate, login, logout, models
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

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
            center_name=registerForm.cleaned_data["center_name"]
            district_name=registerForm.cleaned_data["district_name"]
            key=registerForm.cleaned_data["key"]
            if center_name != "_":
                center_obj=CenterAdmin.objects.get(name=center_name)
                if key==center_obj.centerId.urn[9:]:
                    user=User.objects.create(email=registerForm.cleaned_data["email"])
                    user.aadharNumber=registerForm.cleaned_data["aadharNumber"]
                    user.first_name=registerForm.cleaned_data["first_name"]
                    user.last_name=registerForm.cleaned_data["last_name"]
                    user.set_password(registerForm.cleaned_data["password"])
                    user.is_active = True
                    AccessControlListCenter.objects.create(
                        person=user,
                        centerID=center_obj
                    )
                    user.is_centeradmin=True
                    user.save()
                    return redirect('/loggedin/center/'+center_obj.name)

            if district_name != "_":
                district_obj=DistrictAdmin.objects.get(name=district_name)
                if key==district_obj.districtId.urn[9:]:
                    user=User.objects.create(email=registerForm.cleaned_data["email"])
                    user.aadharNumber=registerForm.cleaned_data["aadharNumber"]
                    user.first_name=registerForm.cleaned_data["first_name"]
                    user.last_name=registerForm.cleaned_data["last_name"]
                    user.set_password(registerForm.cleaned_data["password"])
                    user.is_active = True
                    AccessControlListDistrict.objects.create(
                        person=user,
                        districtID=district_obj
                    )
                    user.is_centeradmin=True
                    user.is_districtadmin=True
                    user.save()
                    return redirect('/loggedin/district/'+district_obj.name)
            else:
                return render(request, "fail.html")
            # user.save()

    else:
        registerForm = RegistrationForm()
    return render(request, "register.html", {"form": registerForm})


def logout(request):
    models.auth.logout(request)
    return redirect('/')
# def register_admin(request):
#     if request.user.is_authenticated:
#         return redirect('provide_access')

#     if request.method == "POST":
#         registerForm = RegistrationForm(request.POST)
#         print("INside post")
#         if registerForm.is_valid():
#             print("Inside form")
#             # user = registerForm.save(commit=False)
#             user=User.objects.create(email=registerForm.cleaned_data["email"])
#             user.aadharNumber=registerForm.cleaned_data["aadharNumber"]
#             user.first_name=registerForm.cleaned_data["first_name"]
#             user.last_name=registerForm.cleaned_data["last_name"]
#             user.set_password(registerForm.cleaned_data["password"])
#             user.is_active = True
#             user.save()
#             return redirect('provide_access')
#     else:
#         registerForm = RegistrationForm()
#     return render(request, "register.html", {"form": registerForm})

# def provide_access(request):
#     if request.user.is_authenticated:
        
#         return redirect('provide_access')
#     else:
#         return redirect('register_admin')
    


# def login_gen(request):
#     if request.user.is_authenticated:
#         return redirect('loggedin')
#     err=""
#     if request.method == 'POST':
#         username = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request, email = username, password = password)
#         if user is not None:
#             models.auth.login(request, user)
#             return redirect('loggedin')
#         else:
#            err = 'Input correct email and password'
#     template_name = 'login.html'
#     context={'err':err}
#     return render(request, template_name,context)



def login_gen(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.user.is_districtadmin:
            access_obj=AccessControlListDistrict.objects.get(person=request.user)
            redirect('/loggedin/district/'+access_obj.districtID.name)
        elif request.user.is_centeradmin:
            access_obj=AccessControlListCenter.objects.get(person=request.user)
            redirect('/loggedin/center/'+access_obj.centerID.name)
        else :
            return redirect('login_gen')
    err=""
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        center = request.POST.get('center')
        district = request.POST.get('district')
        user = authenticate(request, email = username, password = password)

        #TODO add_drop_down and center selection

        if user is not None:
            if center and center!="_":
                center_obj=CenterAdmin.objects.get(name=center)
                if AccessControlListCenter.objects.filter(person=user,centerID=center_obj).exists() and user.is_centeradmin:
                    models.auth.login(request, user)
                    return redirect('/loggedin/center/'+center_obj.name)

                elif AccessControlListDistrict.objects.filter(person=user,districtID=center_obj.district).exists() and user.is_districtadmin:
                    models.auth.login(request, user)
                    return redirect('/loggedin/district/'+center_obj.district.name)
                else:
                    template_name = 'fail.html'
            if district and district!="_":
                district_obj=DistrictAdmin.objects.get(name=district)
                if AccessControlListDistrict.objects.filter(person=user,districtID=district_obj).exists() and user.is_districtadmin:
                    models.auth.login(request, user)
                    return redirect('/loggedin/district/'+district_obj.name)
                else:
                    template_name = 'fail.html'
        else:
           template_name = 'fail.html'
    
    template_name = 'login_center.html'
    context={'err':err}
    return render(request, template_name,context)

@login_required(login_url="login_gen")
def loggedin(request,district_or_center,name):
    # return HttpResponse("user is"+district_or_center+name)
    if district_or_center=="district":
        user=request.user
        if DistrictAdmin.objects.filter(name=name).exists():
            district_obj=DistrictAdmin.objects.get(name=name)
            if AccessControlListDistrict.objects.filter(person=user,districtID=district_obj).exists() and user.is_districtadmin:
                return HttpResponse("user is"+request.user.first_name+" district "+name)
            else:
                return render(request,"fail.html")
        else:
            return render(request,"fail.html")
    elif district_or_center=="center":
        user=request.user
        if CenterAdmin.objects.filter(name=name).exists():
            center_obj=CenterAdmin.objects.get(name=name)
            if AccessControlListCenter.objects.filter(person=user,centerID=center_obj).exists() and user.is_centeradmin:
                return HttpResponse("user is"+request.user.first_name+" Center "+name)

            elif AccessControlListDistrict.objects.filter(person=user,districtID=center_obj.district).exists() and user.is_districtadmin:
                
                return HttpResponse("user is"+request.user.first_name+" district "+name)
            else:
                return render(request,"fail.html")
        else:
            return render(request,"fail.html")
    else:
        return render(request,"fail.html")

@login_required(login_url="login_gen")
def provideaccess(request):
    if request.method == "POST":
        provide_access_form = ProvideAccessForm(request.POST)
        print("INside post")
        if provide_access_form.is_valid():
            print("Inside form")
            # user = registerForm.save(commit=False)
            center_name=provide_access_form.cleaned_data["center_name"]
            district_name=provide_access_form.cleaned_data["district_name"]
            key=provide_access_form.cleaned_data["key"]
            if center_name != "_":
                center_obj=CenterAdmin.objects.get(name=center_name)
                if key==center_obj.centerId.urn[9:]:
                    user=User.objects.get(email=request.user.email)
                    AccessControlListCenter.objects.create(
                        person=user,
                        centerID=center_obj
                    )
                    user.is_centeradmin=True
                    user.save()
                    return redirect('/loggedin/center/'+center_obj.name)
            if district_name != "_":
                district_obj=DistrictAdmin.objects.get(name=district_name)
                if key==district_obj.districtId.urn[9:]:
                    user=User.objects.get(email=request.user.email)
                    AccessControlListDistrict.objects.create(
                        person=user,
                        districtID=district_obj
                    )
                    user.is_centeradmin=True
                    user.is_districtadmin=True
                    user.save()
                    return redirect('/loggedin/district/'+district_obj.name)
            else:
                return render(request, "fail.html")
            # user.save()

    else:
        provide_access_form = ProvideAccessForm()
    return render(request, "provideaccess.html", {"form": provide_access_form})