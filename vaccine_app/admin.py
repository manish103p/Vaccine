from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import VaccineLot, DistrictAdmin, DistrictVaccineData, CenterAdmin, CenterVaccineData, CenterRegestration, Receiver, ReceiverVaccination, AccessControlList
# Register your models here.
from .models import User
admin.site.register(VaccineLot)
admin.site.register(DistrictAdmin)
admin.site.register(DistrictVaccineData)
admin.site.register(CenterAdmin)
admin.site.register(CenterVaccineData)
admin.site.register(CenterRegestration)
admin.site.register(Receiver)
admin.site.register(ReceiverVaccination)
admin.site.register(AccessControlList)




class UserAdminConfig(UserAdmin):
  search_fields=('email','first_name','aadharNumber')
  list_filter=('email', 'is_superuser','is_districtadmin','is_centeradmin')
  ordering=('is_superuser','email')
  list_display=('email','first_name','is_superuser','is_districtadmin','is_centeradmin')
  fieldsets = (
        (None, {'fields': ('email', 'first_name','last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser','is_districtadmin','is_centeradmin')}),
        ('Personal', {'fields': ('aadharNumber',)}),
    )
  add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','last_name','aadharNumber', 'password1', 'password2','is_staff', 'is_active','is_superuser','is_districtadmin','is_centeradmin')}
         ),
    )

admin.site.register(User, UserAdminConfig)
