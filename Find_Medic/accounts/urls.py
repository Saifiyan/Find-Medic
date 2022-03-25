"""Find_Medic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from accounts import views
from django.conf.urls import url  

urlpatterns = [
    
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('Signup', views.Signup, name='Signup'),
    path('Login', views.Login, name='Login'),
    path('Logout', views.Logout, name='Logout'),
    path('View_my_profile', views.updateuserinfo, name='updateuserinfo'),
    path('view_my_request', views.PatientDetailsListView.as_view(), name='ViewMyRequest'),
    path('updateuserprofile', views.updateuserprofile, name='updateuserprofile'),
    path('Uploaduserdetails', views.Uploaduserdetails, name='Uploaduserdetails'),
    path('viewdoctorprofile', views.viewdoctorprofile, name='viewdoctorprofile'),
    path('updatedoctorprofile', views.updatedoctorprofile, name='updatedoctorprofile'),
    path('UploadDoctordetails', views.UploadDoctordetails, name='UploadDoctordetails'),
    path('changedoctorprofile', views.changedoctorprofile, name='changedoctorprofile'),
    path('changeuserprofile', views.changeuserprofile, name='changeuserprofile'),
    #path('BookAppointment', views.BookAppointment, name='BookAppointment'),
    path('BrowseDoctors', views.doctorprofileListView.as_view(), name="BrowseDoctors"),
    #path('edit', views.userprofileListView.as_view(), name="edituser"),
    re_path(r"^BrowseDoctors/(?P<pk>\d+)$", views.doctorprofileDetailView.as_view(), name="doctorprofile-details"),
    url(r'^BrowseDoctors/Give_feedback/(?P<pk>\d+)$', views.givefeedback, name='givefeedback'),
    #path ('BrowseDoctors/User/?P<int:pk>',views.EditUserdetails,name='EditUserdetails'),
    #re_path(r"^edit/(?P<pk>\d+)$", views.userprofileDetailView.as_view(), name="userprofile-details"),
    path('RequestAppointment/?P<int:id>', views.RequestAppointment,name='RequestAppointment'),
    #path('viewuserrequests', views.ViewUserRequest,name='ViewUserRequest'),
    path('viewuserrequests/', views.PatientDetailsListView.as_view(), name="viewuserrequests"),
    re_path(r"^viewuserrequests/(?P<pk>\d+)$", views.PatientDetailsDetailView.as_view(), name="PatientDetails-details"),
    url(r'^viewuserrequests/delete/(?P<pk>\d+)$', views.EditUserdetails, name='EditUserdetails'),  
    url(r'^viewuserrequests/confirm/(?P<pk>\d+)$', views.ConfirmUserRequest, name='ConfirmUserRequest'),  
    url(r'^BrowseDoctors/edit/(?P<pk>\d+)$', views.ChangePatientDetails, name='ChangePatientDetails'),  
    path('generateinvoice/<int:pk>/', views.GenerateInvoice.as_view(), name = 'generateinvoice'),
    path('news/', views.news, name = 'news'),
    path('chat/', views.home, name='chat-home'),
    path('send/', views.send_chat, name='chat-send'),
    path('renew/', views.get_messages, name='chat-renew'),

]

