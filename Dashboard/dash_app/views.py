from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import sys
sys.path.append('MLcodes')

from .models import Doctor, Patient
from .operations.PatientManager import PatientManager
from .operations.details import Details


from backend_brain_pipeline import process_pipeline


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name

def homepage(request):
    details_obj = Details(request=request)
    details = details_obj.get_patient_doctor_details()
    return render(request, "dashboard.html", details)


def results(request):
    details_obj = Details(request=request)
    details = details_obj.get_patient_doctor_details()

    '''
    The bottom code is temporary.
    '''
    patients = details.get('patients')
    details['patient'] = patients[0] 
    ''''''

    paths = ''
    
    fs = OverwriteStorage()
    
    fileObj = request.FILES['filelocation1']
    filePathName1 = fs.save(fileObj.name, fileObj)
    filePathName1 = fs.url(fileObj.name)
    paths = filePathName1
    paths.append("."+filePathName1)
    
    fileObj = request.FILES['filelocation2']
    filePathName2 = fs.save(fileObj.name, fileObj)
    filePathName2 = fs.url(fileObj.name)
    paths.append("."+filePathName2)

    fileObj = request.FILES['filelocation3']
    filePathName3 = fs.save(fileObj.name, fileObj)
    filePathName3 = fs.url(fileObj.name)
    paths.append("."+filePathName3)

    fileObj = request.FILES['filelocation4']
    filePathName4 = fs.save(fileObj.name, fileObj)
    filePathName4 = fs.url(fileObj.name)
    paths.append("."+filePathName4)

    context={'filePathName':filePathName}
    
    print(paths) 
    process_pipeline(paths, fname='dash_app/static/dash_app/mri.gif')

    return render(request, "results.html", details)


def profile(request):
    details_obj = Details(request=request)
    details = details_obj.get_patient_doctor_details()

    '''
    The bottom code is temporary.
    '''
    patients = details.get('patients')
    details['patient'] = patients[0]
    ''''''
    print("PATIENT ", details)
    return render(request, "profile.html", details)

@csrf_exempt
def signin(request):
    print("Signing in user get")
    if request.method == 'POST':
        if request.POST['password_input_type'] and request.POST['email_input_type']:
            try:
                user_email = request.POST['email_input_type']
                password = request.POST['password_input_type']
                print(user_email, password)
                user = User.objects.filter(email=user_email, password=password)
                if user:
                    print('Logging in user: ', user)
                    login(request, user)
                    return HttpResponseRedirect('homepage/dashboard/')
            except Exception as e:
                print("Error while logging ing a user: {}".format(e))
    return render(request, "sign-in.html")


@csrf_exempt
def signup(request):
    print('Signing up user GET')
    if request.method == 'POST':
        """
        Sign up a new user
        """
        if request.POST['password_input_type'] and request.POST['email_input_type'] and request.POST['name_input_type']:
            user_name = request.POST['name_input_type']
            user_email = request.POST['email_input_type']
            password = request.POST['password_input_type']
            try:
                user = User.objects.create_user(username=user_name, email=user_email, password=password)
                user.save()
                doctor = Doctor().create(name=user_name, email=user_email, phone_number=1234567899)
                doctor.save()
                login(request, user)
                return HttpResponseRedirect('homepage/dashboard/')
            except Exception as e:
                print("Error while signing up a user: {}".format(e))
    return render(request, "sign-up.html")


def addpatient(request):

    if request.method == 'POST':
        patient_manager_obj = PatientManager(patient_details=request.POST)
        required_patient_details = patient_manager_obj.all_required_fields_present()
        if required_patient_details:
            patient = Patient().create(
                *required_patient_details
            )
            patient.save()
            # return HttpResponseRedirect('homepage/dashboard/')
    return render(request, "addPatient.html")


def mri(request):

    if request.method == "POST":
        print("uploading")
        mrifiles = request.FILES.getlist("mri")
        print(mrifiles)
        return HttpResponse("ok")