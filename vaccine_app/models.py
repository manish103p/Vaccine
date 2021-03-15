from django.db import models
from datetime import datetime,date    
import os,pytz
from django.utils import timezone
# Create your models here.

lot_status = ( 
    ("produced","produced"), 
    ("atDistrict","atDistrict"), 
    ("atCenter","atCenter"), 
    ("consumed","consumed"), 
) 

class VaccineLot(models.Model):
    lotId = models.AutoField(primary_key=True)
    status=models.CharField(max_length = 10, choices = lot_status, default = 'produced')
    productionTimestamp = models.DateTimeField(auto_now_add=True)
    departureTimestamp = models.DateTimeField()


class DistrictAdmin(models.Model):
    districtId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=20)

class DistrictVaccineData(models.Model):
    district = models.ForeignKey(DistrictAdmin,on_delete=models.CASCADE,related_name="districtVaccine")
    lot = models.OneToOneField(VaccineLot, on_delete=models.CASCADE,related_name="districtVaccine")
    arrivalTimestamp = models.DateTimeField(auto_now_add=True)
    departureTimestamp = models.DateTimeField()

class CenterAdmin(models.Model):
    centerId = models.AutoField(primary_key=True)
    district = models.ForeignKey(DistrictAdmin,on_delete=models.CASCADE,related_name="centerAdmin")
    userName = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=20)

class CenterVaccineData(models.Model):
    center = models.ForeignKey(CenterAdmin,on_delete=models.CASCADE,related_name="centerVaccine")
    lot = models.OneToOneField(VaccineLot, on_delete=models.CASCADE,related_name="centerVaccine")
    arrivalTimestamp = models.DateTimeField(auto_now_add=True)
    departureTimestamp = models.DateTimeField()

class CenterRegestration(models.Model):
    center = models.OneToOneField(CenterAdmin,on_delete=models.CASCADE,related_name="centerRegestrations")
    count = models.IntegerField()

class Receiver(models.Model):
    aadharNumber = models.CharField(max_length=16, unique=True, primary_key=True)
    center = models.ForeignKey(CenterAdmin,on_delete=models.CASCADE,related_name="receiver")
    name = models.CharField(max_length=255)
    contactNumber= models.CharField(max_length=12, )
    address = models.CharField(max_length=1000, null = True)
    email = models.EmailField()

class ReceiverVaccination(models.Model):
    receiver = models.OneToOneField(Receiver, on_delete=models.CASCADE,related_name="receiverVaccination")
    lot = models.OneToOneField(VaccineLot, on_delete=models.CASCADE,related_name="receiverVaccination")
    appointmentDate=models.DateField(auto_now_add=True)
    vaccineDose=models.BooleanField(default = False)
