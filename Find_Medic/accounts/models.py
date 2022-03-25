from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
from datetime import date, datetime

# Create your models here.

class userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    age = models.IntegerField()
    dob = models.DateField()
    gender = models.CharField(max_length=6)
    bgroup = models.CharField(max_length=10)
    contno = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse("userprofile-details", args=[str(self.id)])

    def __str__(self):
        return self.user.username

class usertype(models.Model):
    usertype = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)

class doctorprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    photo = models.FileField(upload_to='docpics')
    gender = models.CharField(max_length=6)
    specialist = models.CharField(max_length=50)
    degree = models.CharField(max_length=100)
    licence = models.FileField(upload_to='docpics')
    contno = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    fee = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    Upload_Profile = models.BooleanField(default=False)
    Clinic_or_Hospital_name = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ('city',)
        
    def get_absolute_url(self):
        return reverse("doctorprofile-details", args=[str(self.id)])#kwargs={"pk": self.pk}
    

    def __str__(self):
        return self.user.username


class OnOffDoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    check = models.BooleanField(default=True)


class PatientDetails(models.Model):
    name = models.CharField(max_length=100)
    doctorname = models.CharField(max_length=100, null=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=6)
    bgroup = models.CharField(max_length=4)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    did = models.IntegerField()
    pid = models.IntegerField(default=False)
    date = models.DateField()
    time = models.TimeField()
    request = models.BooleanField(default=False)
    nowdatetime = models.CharField(max_length=100, null=True)
    daddress = models.CharField(max_length=100, null=True)
    dcontact = models.CharField(max_length=15, null=True)
    demail = models.CharField(max_length=50, null=True)
    dcity = models.CharField(max_length=50, null=True)
    dstate = models.CharField(max_length=50, null=True)
    dfee = models.CharField(max_length=50, null=True)
    give_a_message = models.TextField(null=True, blank=True)
    purpose_of_meeting = models.TextField()
    payment = models.CharField(max_length=1)
    Clinic_or_Hospital_name = models.CharField(max_length=100, blank=True)
                                      

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("PatientDetails-details", args=[str(self.id)])

    class Meta:
        ordering = ('-date','-time',)    


    @property
    def is_past_due(self):
        return date.today() == self.date

    @property
    def dategone(self):
        return date.today() > self.date

    @property
    def datecome(self):
        return date.today() <= self.date

    @property
    def timegone(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(now)
        timestored = self.time
        if current_time > timestored and date.today() == self.date:
            return True
        else:
            return False

class News(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField()
    image = models.ImageField(upload_to='newspics', null=True)
    link = models.TextField(null=True)
    datetimenow = models.DateTimeField() 

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('datetimenow',)

from django.utils import timezone

class chatMessages(models.Model):
    user_from = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="+")
    user_to = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="+")
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message