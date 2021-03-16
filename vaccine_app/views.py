from django.shortcuts import render,redirect
from django.http import HttpResponse
# from django.contrib.auth.models import  User,auth
from .models import VaccineLot, DistrictAdmin, DistrictVaccineData, CenterAdmin, CenterVaccineData, CenterRegestration, Receiver, ReceiverVaccination
from datetime import datetime

# Create your views here.
def index(request):
    return render(request,"index.html")