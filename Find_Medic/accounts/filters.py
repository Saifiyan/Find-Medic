import django_filters
from .models import doctorprofile


class DoctorFilters(django_filters.FilterSet):
    class Meta:
        model = doctorprofile
        fields = {
            'Clinic_or_Hospital_name' : ['icontains'],
            'city' : ['icontains'],
            'state' : ['icontains'],
            'specialist' : ['icontains'],
            'gender' : ['icontains'],
        }