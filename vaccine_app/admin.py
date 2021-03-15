from django.contrib import admin
from .models import VaccineLot, DistrictAdmin, DistrictVaccineData, CenterAdmin, CenterVaccineData, CenterRegestration, Receiver, ReceiverVaccination
# Register your models here.

admin.site.register(VaccineLot)
admin.site.register(DistrictAdmin)
admin.site.register(DistrictVaccineData)
admin.site.register(CenterAdmin)
admin.site.register(CenterVaccineData)
admin.site.register(CenterRegestration)
admin.site.register(Receiver)
admin.site.register(ReceiverVaccination)




