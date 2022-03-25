from django import forms
from django.contrib.auth.models import User
from .models import userprofile, doctorprofile, PatientDetails
#Unused User imported from django.contrib.auth.models
#class userprofileform(forms.ModelForm):
#    class meta:
#        model = userprofile
#        fields = ('age', 'dob' , 'gender', 'bgroup', 'contno', 'address', 'city', 'state')

#class DoctForm(forms.ModelForm):
#    class Meta:
#        model = doctorprofile
#        fields = ('user', 'photo', 'gender', 'specialist', 'degree', 'licence', 'contno' ,'address' ,'fee', 'city', 'state')

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','email']

class UpdateDoctorProfile(forms.ModelForm):
    class Meta:
        model = doctorprofile
        fields = ['photo', 'gender', 'specialist', 'degree','licence', 'contno', 'address', 'fee', 'city', 'state', 'Clinic_or_Hospital_name','Upload_Profile',]

class UpdateUserProfile(forms.ModelForm):
    class Meta:
        model = userprofile
        fields = ['age', 'dob', 'gender', 'bgroup', 'contno', 'address', 'city', 'state']

class AcceptUserRequest(forms.ModelForm):
    class Meta:
        model = PatientDetails
        fields = ['date','time','request','give_a_message',]

class ChangeUserRequest(forms.ModelForm):
    class Meta:
        model = PatientDetails
        fields = ['name','age','gender','bgroup','email','contact','address','city','state','purpose_of_meeting']