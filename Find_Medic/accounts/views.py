from dateutil.parser import parse
import os
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from io import BytesIO
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.core.files.storage import FileSystemStorage
from .forms import UpdateDoctorProfile, UserUpdateForm, UpdateUserProfile, AcceptUserRequest, ChangeUserRequest
from django.contrib.auth.decorators import login_required
from django.views import generic
import datetime
from django.views.generic.edit import DeleteView, View
from django.conf import settings
from .filters import DoctorFilters
from django.core.paginator import Paginator
from datetime import date

# @property
# def format_time(self):
#    t = datetime.datetime.now()
#    s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
#    now = s[:-16]
#    return now == self.object.date
# def is_past_due(self):
# return date.today() == self.date


# Create your views here.

def news(request):
    newsobj = News.objects.all()
    return render(request, 'news.html', {'newsobj': newsobj})

def chat(request):
    users = User.objects.all()
    appt = PatientDetails.objects.all()
    context = {
        'users':users,
        'appt':appt,
    }
    return render(request, 'home.html', context)

import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserModel
from django.db.models import Q

def get_messages(request):
    chats = chatMessages.objects.filter(Q(id__gt=request.POST['last_id']),Q(user_from=request.user.id, user_to=request.POST['chat_id']) | Q(user_from=request.POST['chat_id'], user_to=request.user.id))
    new_msgs = []
    for chat in list(chats):
        data = {}
        data['id'] = chat.id
        data['user_from'] = chat.user_from.id
        data['user_to'] = chat.user_to.id
        data['message'] = chat.message
        data['date_created'] = chat.date_created.strftime("%b-%d-%Y %H:%M")
        new_msgs.append(data)
    return HttpResponse(json.dumps(new_msgs), content_type="application/json")

def send_chat(request):
    resp = {}
    User = get_user_model()
    if request.method == 'POST':
        post =request.POST
        
        u_from = UserModel.objects.get(id=post['user_from'])
        u_to = UserModel.objects.get(id=post['user_to'])
        insert = chatMessages(user_from=u_from,user_to=u_to,message=post['message'])
        try:
            insert.save()
            resp['status'] = 'success'
        except Exception as ex:
            resp['status'] = 'failed'
            resp['mesg'] = ex
    else:
        resp['status'] = 'failed'

    return HttpResponse(json.dumps(resp), content_type="application/json")


def home(request):
    User = get_user_model()
    users = User.objects.all()
    appt = PatientDetails.objects.all()
    chats = {}
    if request.method == 'GET' and 'u' in request.GET:
        # chats = chatMessages.objects.filter(Q(user_from=request.user.id & user_to=request.GET['u']) | Q(user_from=request.GET['u'] & user_to=request.user.id))
        chats = chatMessages.objects.filter(Q(user_from=request.user.id, user_to=request.GET['u']) | Q(user_from=request.GET['u'], user_to=request.user.id))
        chats = chats.order_by('date_created')
    context = {
        "page":"home",
        "users":users,
        "appt":appt,
        "chats":chats,
        "chat_id": int(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    }
    return render(request,"home.html",context)




def Login(request):
    if request.method == 'POST':
        login_username = request.POST['usernamel']
        login_password = request.POST['passwordl']

        user = auth.authenticate(
            username=login_username, password=login_password)

        if user is not None:
            auth.login(request, user)
            #print('\n user logged in \n')
            messages.info(request, 'You logged in')
            return redirect('/Find_Medic/BrowseDoctors')
        else:
            #print('\n invalid credentials \n')
            messages.error(request, 'Invalid credentials')
            return redirect('/Find_Medic/login')

    else:
        return redirect('/Find_Medic/login')


def Logout(request):
    auth.logout(request)
    #print('\n User logged out\n')
    messages.info(request, 'You logged out')
    return redirect('/Find_Medic/')


# for generating pdf invoice


def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    # , link_callback=fetch_resources)
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GenerateInvoice(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            uid = request.user.id
            # you can filter using order_id as well
            pdetails = PatientDetails.objects.get(id=pk, request=True, pid=uid)
        except:
            return HttpResponse("505 Not Found")
        data = {
            'id': pdetails.id,
            'doctorname': pdetails.doctorname,
            'name': pdetails.name,
            'age': pdetails.age,
            'gender': pdetails.gender,
            'bloodgroup': pdetails.bgroup,
            'contact': pdetails.contact,
            'email': pdetails.email,
            'address': pdetails.address,
            'city': pdetails.city,
            'state': pdetails.state,
            'request': pdetails.request,
            'pid': pdetails.pid,
            'date': pdetails.date,
            'time': pdetails.time,
            'nowdatetime': pdetails.nowdatetime,
            'daddress': pdetails.daddress,
            'dcontact': pdetails.dcontact,
            'demail': pdetails.demail,
            'dcity': pdetails.dcity,
            'dstate': pdetails.dstate,
            'dfee': pdetails.dfee,

        }
        pdf = render_to_pdf('accounts/recipt/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

        # if pdf:
        #     response = HttpResponse(pdf, content_type='application/pdf')
        #     filename = "Invoice_%s.pdf" %(data['id'])
        #     content = "inline; filename='%s'" %(filename)
        #     #download = request.GET.get("download")
        #     #if download:
        #     content = "attachment; filename=%s" %(filename)
        #     response['Content-Disposition'] = content
        #     return response
        # return HttpResponse("Not found")


# def listing(request):
#     contact_list = doctorprofile.objects.all()
#     paginator = Paginator(contact_list, 4) # Show 25 contacts per page.

#     page_number = request.GET.get('city')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'doctorprofile_list.html', {'filter.qs': page_obj})


def signup(request):

    return render(request, 'signup.html')


def index(request):

    #useru18 = PatientDetails.objects.filter(id=4)
    # useru16.delete()

    return render(request, 'DocProfileOnMainPage.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('/Find_Medic/')
    else:
        return render(request, 'login.html')


def Signup(request):
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        gmail = request.POST['gmail']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        usertyp = request.POST['usertype']
        pas = password

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Sorry! Username is taken')
            return redirect('/Find_Medic/signup')

        elif User.objects.filter(email=gmail).exists():

            messages.error(request, 'Sorry! email is taken')
            return redirect('/Find_Medic/signup')

        elif name == "":
            messages.error(request, 'Please enter your name!')
            return redirect('/Find_Medic/signup')

        elif username == "":
            messages.error(request, 'Please enter your username!')
            return redirect('/Find_Medic/signup')

        elif gmail == "":
            messages.error(request, 'Please enter your Email!')
            return redirect('/Find_Medic/signup')

        elif password == "":
            messages.error(request, 'Please enter your Password!')
            return redirect('/Find_Medic/signup')

        elif len(pas) < 8:
            messages.error(request, 'Password must contain 8 characters!')
            return redirect('/Find_Medic/signup')

        elif pas.isdecimal():
            messages.error(
                request, 'Password must contain atleast one character!')
            return redirect('/Find_Medic/signup')

        elif password != confirmpassword:
            messages.error(request, 'Password does not matched')
            return redirect('/Find_Medic/signup')

        else:
            user = User.objects.create_user(
                first_name=name, email=gmail, username=username, password=password)
            user.save()
            user_type = usertype(user=user, usertype=usertyp)
            user_type.save()
            messages.info(request, 'Account created successfully.')
            return redirect('/Find_Medic/login')
    else:
        return render(request, 'signup.html')


# redirect when user is not logged in
@login_required(login_url='/Find_Medic/login')
def updateuserinfo(request):
    user = request.user
    if user.usertype.usertype == "user":
        return render(request, 'userprofile.html')
    else:
        return HttpResponse("You are not a User")


# redirect when user is not logged in
@login_required(login_url='/Find_Medic/login')
def Uploaduserdetails(request):
    if request.method == 'POST':
        userm = request.user
        dob = request.POST['dob']
        age = request.POST['age']
        gender = request.POST['gender']
        blood = request.POST['bgroup']
        contno = request.POST['contno']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']

        useru = userprofile(user=userm, dob=dob, age=age, gender=gender,
                            bgroup=blood, contno=contno, address=address, city=city, state=state)
        useru.save()
        messages.info(request, 'Details Uploaded Successfully!')
        return redirect('/Find_Medic/View_my_profile')
    else:
        return HttpResponse("505 not found")


# redirect when user is not logged in
@login_required(login_url='/Find_Medic/login')
def UploadDoctordetails(request):
    if request.method == 'POST' and request.FILES['photo'] and request.FILES['licence']:

        photo = request.FILES['photo']
        licence = request.FILES['licence']
        clname = request.POST['chname']

        #fsp = FileSystemStorage()
        #fsl = FileSystemStorage()
        #photo_name = fsp.save(photo.name, photo)
        #licence_name = fsl.save(licence.name, licence)
        #urlp = fsp.url(photo_name)
        #urll = fsl.url(licence_name)

        docprofile = doctorprofile(
            user=request.user,
            photo=photo,
            gender=request.POST['gender'],
            specialist=request.POST['specialist'],
            degree=request.POST['degree'],
            licence=licence,
            contno=request.POST['contno'],
            address=request.POST['address'],
            fee=request.POST['fee'],
            city=request.POST['city'],
            state=request.POST['state'],
            Upload_Profile=request.POST['Upload_Profile'],
            Clinic_or_Hospital_name=request.POST['chname'],
        )
        docprofile.save()
        messages.info(request, 'Details Uploaded Successfully!')
        return redirect('/Find_Medic/viewdoctorprofile')
    else:
        return HttpResponse("505 not found")


# redirect when user is not logged in
@login_required(login_url='/Find_Medic/login')
def updateuserprofile(request):
    user = request.user
    if user.usertype.usertype == "user":
        return render(request, 'updateuserprofile.html')
    else:
        return HttpResponse("You are not a User")


# redirect when user is not logged in
@login_required(login_url='/Find_Medic/login')
def viewdoctorprofile(request):
    user = request.user
    if user.usertype.usertype == "doctor":
        return render(request, 'viewdoctorprofile.html')
    else:
        return HttpResponse("You are not a Doctor")


# redirect when user is not logged in
@login_required(login_url='/Find_Medic/login')
def updatedoctorprofile(request):
    user = request.user
    if user.usertype.usertype == "doctor":
        return render(request, 'updatedoctorprofile.html')
    else:
        return HttpResponse("You are not a Doctor")


# redirect when user is not logged in
@login_required(login_url='/Find_Medic/login')
def changedoctorprofile(request):
    user = request.user
    if request.method == 'POST':

        if user.usertype.usertype == "doctor":
            u_form = UserUpdateForm(request.POST, instance=request.user)
            d_form = UpdateDoctorProfile(
                request.POST, request.FILES, instance=request.user.doctorprofile)

            if u_form.is_valid() and d_form.is_valid():
                u_form.save()
                d_form.save()
                messages.info(request, 'Changes Applied Successfully!')
                return redirect('/Find_Medic/viewdoctorprofile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        d_form = UpdateDoctorProfile(instance=request.user.doctorprofile)

    context = {
        'u_form': u_form,
        'd_form': d_form
    }

    return render(request, 'changedoctorprofile.html', context)


# redirect when user is not logged in
@login_required(login_url='/Find_Medic/login')
def changeuserprofile(request):
    user = request.user
    if request.method == 'POST':

        if user.usertype.usertype == "user":
            uu_form = UserUpdateForm(request.POST, instance=request.user)
            up_form = UpdateUserProfile(
                request.POST, instance=request.user.userprofile)

            if uu_form.is_valid() and up_form.is_valid():
                uu_form.save()
                up_form.save()
                messages.info(request, 'Changes Applied Successfully!')
                return redirect('/Find_Medic/View_my_profile')
        elif user.usertype.usertype == "doctor":
            return redirect('/Find_Medic/')

    else:
        uu_form = UserUpdateForm(instance=request.user)
        up_form = UpdateUserProfile(instance=request.user.userprofile)

    context = {
        'uu_form': uu_form,
        'up_form': up_form
    }

    return render(request, 'changeuserprofile.html', context)


# @login_required(login_url='/Find_Medic/signup') #redirect when user is not logged in
# def BookAppointment(request):
#     return render(request, 'BookAppoitment.html')

class doctorprofileListView(generic.ListView):
    model = doctorprofile
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = DoctorFilters(
            self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return DoctorFilters(self.request.GET, queryset=queryset).qs


class doctorprofileDetailView(generic.DetailView):
    model = doctorprofile


class userprofileListView(generic.ListView):
    template_name = 'userprofile_list.html'
    model = PatientDetails


class userprofileDetailView(generic.DetailView):
    model = userprofile


class PatientDetailsListView(generic.ListView):
    model = PatientDetails
    # print(date.today())
    # @property
    # def is_past_due(self):
    #     return date.today() > self.date.date()


class PatientDetailsDetailView(generic.DetailView):
    model = PatientDetails


# redirect when user is not logged in
@login_required(login_url='/Find_Medic/login')
def EditUserdetails(request, pk):
    if request.user.is_superuser:
        movies = get_object_or_404(PatientDetails, pk=pk)
    else:
        movies = get_object_or_404(PatientDetails, pk=pk)
    if request.method == 'POST':
        movies.delete()
        return redirect('/Find_Medic/viewuserrequests')
    return render(request, 'confirm_delete.html', {'object': movies})


# redirect when user is not logged in
@login_required(login_url='/Find_Medic/login')
def ConfirmUserRequest(request, pk):
    if request.user.is_superuser:
        movies = get_object_or_404(PatientDetails, pk=pk)
    else:
        movies = get_object_or_404(PatientDetails, pk=pk)
    form = AcceptUserRequest(request.POST or None, instance=movies)
    formN = ChangeUserRequest(request.POST or None, instance=movies)
    if form.is_valid():
        form.save()
        return redirect('PatientDetails-details', pk)
    elif formN.is_valid():
        formN.save()
        return redirect('PatientDetails-details', pk)

    return render(request, 'confirm_request.html', {'form': form, 'formN': formN, 'object': movies})


# redirect when user is not logged in
@login_required(login_url='/Find_Medic/login')
def ChangePatientDetails(request, pk):
    if request.user.is_superuser:
        movies = get_object_or_404(doctorprofile, pk=pk)
    else:
        movies = get_object_or_404(doctorprofile, pk=pk)
    if request.method == 'POST':
        return redirect('/Find_Medic/viewuserrequests')
    return render(request, 'changepatientdetais.html', {'object': movies})


# redirect when user is not logged in
@login_required(login_url='/Find_Medic/login')
def RequestAppointment(request, id):
    uuid = request.user.id
    if request.method == 'POST':
        name = request.POST['pname']
        age = request.POST['page']
        gender = request.POST['pgender']
        bgroup = request.POST['pbgroup']
        contno = request.POST['pcontact']
        email = request.POST['pemail']
        address = request.POST['paddress']
        city = request.POST['pcity']
        did = request.POST['did']
        state = request.POST['pstate']
        date = request.POST['pdate']
        time = request.POST['ptime']
        doctorname = request.POST['doctorname']
        daddress = request.POST['daddress']
        dcontact = request.POST['dcontact']
        demail = request.POST['demail']
        dcity = request.POST['dcity']
        dstate = request.POST['dstate']
        dfee = request.POST['dfee']
        purpose_of_meeting = request.POST['purpose_of_meeting']
        payment = request.POST['chk']
        Clinic_or_Hospital_name = request.POST['chname']

        def format_time():
            t = datetime.datetime.now()
            s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
            return s[:-16]

        def timea():
            t = datetime.datetime.now()
            s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
            return s[10:-7]
        details = PatientDetails(
            name=name,
            age=age,
            gender=gender,
            bgroup=bgroup,
            contact=contno,
            email=email,
            address=address,
            city=city,
            state=state,
            did=did,
            pid=uuid,
            date=date,
            time=time,
            nowdatetime=format_time(),
            doctorname=doctorname,
            daddress=daddress,
            dcontact=dcontact,
            demail=demail,
            dcity=dcity,
            dstate=dstate,
            dfee=dfee,
            purpose_of_meeting=purpose_of_meeting,
            payment=payment,
            Clinic_or_Hospital_name=Clinic_or_Hospital_name,
        )
        # a = int(time)
        dateR = parse(date)
        dateT = parse(format_time())
        timeR = parse(time)
        timeT = parse(timea())
        # print(date2 > date2)
        # date2 = PatientDetails.objects.filter(date=date)
        # print(date2)
        # at = date2.str('%Y-%m-%d')
        # date3 = parse(at)
        print(dateR)
        print(dateT)
        print(timeR)
        print(timeT)
        # if dateT>dateR and time

        if dateR < dateT and timeR < timeT:
            messages.info(request, 'Time and date you took is a past!')
            return redirect('doctorprofile-details', id)

        elif timeR < timeT and dateR == dateT:
            messages.info(request, 'Time you took is a past!')
            return redirect('doctorprofile-details', id)

        elif timeR > timeT and dateR < dateT:
            messages.info(request, 'Time you took is a past!')
            return redirect('doctorprofile-details', id)

        elif PatientDetails.objects.filter(name=name, did=did, pid=uuid, gender=gender, contact=contno, email=email, age=age, bgroup=bgroup, address=address, city=city, request=False):
            messages.info(request, 'Your appointment is under request')
            return redirect('doctorprofile-details', id)

        # elif PatientDetails.objects.filter(name=name, did=did, pid=uuid, gender=gender, contact=contno, age=age, bgroup=bgroup, address=address, city=city, request= True, date=<dateR):
        #     messages.info(request, 'Your appointment is under ')
        #     return redirect('/Find_Medic/BrowseDoctors')
        # elif PatientDetails.objects.filter(name=name, did=did, pid=uuid, request=True):
        #     messages.info(request, 'OK')
        #     return redirect('/Find_Medic/BrowseDoctors')

        elif PatientDetails.objects.filter(did=did, date=date, time=time):
            messages.info(
                request, 'Appointment date and time is booked try another time')
            return redirect('doctorprofile-details', id)

        # elif PatientDetails.objects.filter(date=format_time()):
        #    movies = get_object_or_404(PatientDetails, id=id)
        #    movies.delete()

        else:
            details.save()
            messages.info(request, 'Request Sent Successfully!')
            return render(request, 'success_request.html')


# redirect when user is not logged in
@login_required(login_url='/Find_Medic/login')
def ViewUserRequest(request):
    user = request.user
    uid = user.id

    if request.method == 'POST':
        r_form = AcceptUserRequest(request.POST, instance=PatientDetails)
        if r_form.is_valid():
            r_form.save()
            messages.info(request, 'Request Accepted Successfully!')
            return redirect('/Find_Medic/viewdoctorprofile')

    else:
        r_form = AcceptUserRequest(instance=PatientDetails)

    context = {
        'r_form': r_form
    }

    return render(request, 'view_user_request.html', context)


def givefeedback(request):
    return render(request, 'feedback.html')
