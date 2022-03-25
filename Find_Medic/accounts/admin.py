from django.contrib import admin
from .models import userprofile, doctorprofile, PatientDetails, News
# Register your models here.
admin.site.register(userprofile)
admin.site.register(doctorprofile)
admin.site.register(PatientDetails)
admin.site.register(News)