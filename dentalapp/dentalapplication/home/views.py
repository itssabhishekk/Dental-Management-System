import profile
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Service
from .models import Doctor
from .models import PatientUser
from .models import Appointment 
from .models import Report 
from .forms import AppointmentForm, UpdatePatientForm, UpdatePatientUserForm, UserAppointmentForm
from .forms import DoctorForm
from .forms import ReportForm
from .forms import PatientUserForm
from .forms import PatientForm
from .forms import ServiceForm
from .forms import ContactForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test





#View for Home page. Created a contact form for the contact us page.
def home(request):
    form = ContactForm()
    if request.method == "POST" or None:
        form = ContactForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form successfully submitted. Our team will reach out to you soon.')
            return HttpResponseRedirect('/#')
    context = {'form': form}
    return render(request, 'home.html', context) 

#View for User Registration page. 
def signup(request):
    userForm=PatientUserForm()
    patientForm=PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=PatientUserForm(request.POST)
        patientForm=PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save()
            patient.user=user
            patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT') #Setting user type as patient.
            my_patient_group[0].user_set.add(user)
        else:
            messages.error(request, 'Invalid Details! Please fill again.')
            return redirect('/signup')
        messages.success(request, 'Account Successfully Created. Please Log in.')
        return HttpResponseRedirect('login')
    return render(request,'signup.html',context=mydict)

#View for Logout. 
def logout(request):
    auth.logout(request)
    return redirect('/login')

#To compare whether the user is admin or patient for the authentication. 
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


#View for User Login page and validation. 
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/userdashboard")
        else:
            messages.error(request, 'Invalid credentials !')
            return redirect('/login')
    else:
        return render(request, 'login.html')
        
#View for Admin Login page and validation. 
def adminlogin(request):
    if request.method == "POST":
        username = request.POST['adminusername']
        password = request.POST['adminpassword']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/admindashboard")
        else:
            messages.error(request, 'Invalid credentials !')
            return redirect('/adminlogin')
    else:
        return render(request, 'adminlogin.html')

#For User Side

#For the base of the user that is the side bar.
@login_required(login_url='/login') #Decorators for authentication
@user_passes_test(is_patient) #Checking if the user is patient or not
def userbase(request):
    patientUser = PatientUser.objects.get(user=request.user.id) #To get the profile picture of user in the side bar.
    return render(request, 'userbase.html', {'patientUser': patientUser})


#View for User Dashboard. Calculating the total count of report of user, user's finished and pending appointment and the doctor and service count available.
@login_required(login_url='/login')
@user_passes_test(is_patient)
def userdashboard(request):
    patientUser = PatientUser.objects.get(user=request.user.id)
    doctorscount=Doctor.objects.all().count()
    reportcount=Report.objects.filter(appointment__patientUser=patientUser).all().count()
    servicecount=Service.objects.all().count()
    appointment=Appointment.objects.all().filter(patientUser=patientUser,status=1)
    finishedappointmentcount = Appointment.objects.all().filter(patientUser=patientUser, status=4).count()
    pendingappointmentcount = Appointment.objects.all().filter(patientUser=patientUser,status=0 ).count()
    mydict={
    'appointment': appointment,
    'patientUser':patientUser,
    'doctorscount':doctorscount,
    'reportcount': reportcount, 
    'servicecount': servicecount,
    'finishedappointmentcount':finishedappointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'userdashboard.html', mydict)


#View for User Appointment Page where user can navigate through appointment views.
@login_required(login_url='/login')
@user_passes_test(is_patient)
def userappointment(request):
    patientUser = PatientUser.objects.get(user=request.user.id)
    return render(request,'userappointment.html', {'patientUser':patientUser})

#View for User Appointment Form Page and validation. 
@login_required(login_url='/login')
@user_passes_test(is_patient)
def user_book_appointment(request):
    form = UserAppointmentForm()
    patientUser = PatientUser.objects.get(user_id=request.user.id)
    if request.method == "POST":
        form = UserAppointmentForm(request.POST)
        if form.is_valid():
            appointment=form.save(commit=False)
            appointment.patientUser=patientUser
            appointment.status = 0
            appointment.save()
            messages.success(request, 'Booking done successfully. Please wait for approval.')
            return HttpResponseRedirect('/user_view_appointment')            

    return render(request,'user_book_appointment.html', {'form':form, 'patientUser':patientUser,})

#View for seeing all of user's appointment.
@login_required(login_url='/login')
@user_passes_test(is_patient)
def user_view_appointment(request):
    patientUser = PatientUser.objects.get(user=request.user.id) #to get the profile picture in the sidebar
    appointment = Appointment.objects.filter(patientUser=patientUser).all()
    return render(request,'user_view_appointment.html', {'appointment':appointment ,'patientUser':patientUser})

#View for seeing all the doctors available.
@login_required(login_url='/login')
@user_passes_test(is_patient)
def user_view_doctors(request):
    patientUser = PatientUser.objects.get(user=request.user.id)
    doctors = Doctor.objects.all
    return render(request,'user_view_doctors.html',{'doctors':doctors ,'patientUser':patientUser})

#View for seeing all of user's report.
@login_required(login_url='/login')
@user_passes_test(is_patient)
def user_view_reports(request):
    patientUser = PatientUser.objects.get(user=request.user.id)
    reports = Report.objects.filter(appointment__patientUser=patientUser).all()
    return render(request,'user_view_reports.html', {'reports':reports , 'patientUser':patientUser})

#View for seeing all of the services available.
@login_required(login_url='/login')
@user_passes_test(is_patient)
def user_view_services(request):
    patientUser = PatientUser.objects.get(user=request.user.id)
    services = Service.objects.all
    return render(request,'user_view_services.html', {'services':services , 'patientUser':patientUser})

#View for seeing all of user's profile.
@login_required(login_url='/login')
@user_passes_test(is_patient)
def user_view_profile(request):
    patientUser = PatientUser.objects.get(user=request.user.id)
    Patient = PatientUser.objects.filter(user=request.user)
    return render(request,'user_view_profile.html', {'patientUser':patientUser, 'Patient':Patient})

#View to cancel user's pending or confirmed appointment.
@login_required(login_url='/login')
@user_passes_test(is_patient)
def user_cancel_appointment(request, pk):
    appointments = Appointment.objects.get(pk=pk)
    appointments.status=3
    appointments.save()
    messages.warning(request, 'Booking cancelled.')
    return redirect('user_view_appointment')

#View for user to edit their data and its validation.
@login_required(login_url='/login')
@user_passes_test(is_patient)
def user_edit_profile(request):
    patientUser = PatientUser.objects.get(user=request.user.id) #to get the profile picture in the sidebar
    u_form = UpdatePatientUserForm(instance=request.user)
    p_form = UpdatePatientForm(instance=request.user.patientuser)
    if request.method == "POST":
        u_form = UpdatePatientUserForm(request.POST, instance=request.user)
        p_form = UpdatePatientForm(request.POST, request.FILES, instance=request.user.patientuser)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Account successfully updated.')
            return redirect('user_view_profile')
            
    context = { 'u_form': u_form, 'p_form': p_form, 'patientUser':patientUser }
    return render(request, 'user_edit_profile.html', context)
 

#For Admin Side



#For the base of the user that is the side bar.
@login_required(login_url='/adminlogin') #Decorators for authentication
@user_passes_test(is_admin) #Checking if the user is admin or not
def adminbase(request):
    return render(request, 'adminbase.html')

#Admin's dashboard where we can see the total doctor, service, patient and appointment count along with the upcoming appointments.
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def admindashboard(request):
    appointment=Appointment.objects.all().order_by('-id').filter(status=1)
    doctorcount=Doctor.objects.all().count()
    patientcount=PatientUser.objects.all().count()
    servicecount=Service.objects.all().count()
    appointmentcount = Appointment.objects.all().filter(status__gte=1).count()
    pendingappointmentcount = Appointment.objects.all().filter(status=0).count()
    mydict={
    'appointment':appointment,
    'doctorcount':doctorcount,
    'patientcount': patientcount, 
    'servicecount': servicecount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'admindashboard.html', context=mydict)

#View for Admin Appointment Page where user can navigate through appointment views.
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def adminappointment(request):
    return render(request,'adminappointment.html')


#View for Admin Appointment Form Page and validation. 
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def admin_book_appointment(request):
    form=AppointmentForm()
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking done successfully. Please review it.')
            return HttpResponseRedirect('/admin_approve_appointment')

    return render(request,'admin_book_appointment.html', {'form':form})

#View for seeing all of user appointment.
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment(request):
    appointments = Appointment.objects.all().filter(status__gte=1)
    return render(request,'admin_view_appointment.html', {'appointment':appointments})

#View for deleting the selected appointment.
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def delete_appointment (request, pk):
    appointments = Appointment.objects.get(pk=pk)
    appointments.delete()
    messages.danger(request, 'Appointment deleted.')
    return redirect('admin_view_appointment')

#View for viewing all the pending appointment list.
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment(request):
    appointments = Appointment.objects.all().filter(status=0)
    return render(request,'admin_approve_appointment.html', {'appointment':appointments})

#View for approving the pending appointment.
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def approve_appointment(request, pk):
    appointments = Appointment.objects.get(pk=pk)
    appointments.status=1
    appointments.save()
    messages.success(request, 'Booking approved.')
    return redirect('admin_view_appointment')

#View for rejecting the pending appointment.
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def reject_appointment(request, pk):
    appointments = Appointment.objects.get(pk=pk)
    appointments.status=2
    appointments.save()
    messages.warning(request, 'Booking rejected.')
    return redirect('admin_view_appointment')

#View for canceling the confirmed appointment.
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def admin_cancel_appointment(request, pk):
    appointments = Appointment.objects.get(pk=pk)
    appointments.status=3
    appointments.save()
    messages.warning(request, 'Booking cancelled.')
    return redirect('admin_view_appointment')

#View for finishing the finished appointment.
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def finish_appointment(request, pk):
    appointments = Appointment.objects.get(pk=pk)
    appointments.status=4
    appointments.save()
    messages.success(request, 'Booking finished.')
    return redirect('admin_view_appointment')

#View for viewing all the doctors in the database.
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def admin_view_doctors(request):
    doctors = Doctor.objects.all
    return render(request,'admin_view_doctors.html',{'doctors':doctors})

#View for removing the doctor from the database.
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def delete_doctor(request, pk):
    doctors = Doctor.objects.get(pk=pk)
    doctors.delete()
    messages.warning(request, 'Doctor removed.')
    return redirect('admin_view_doctors')


#View for adding doctors to the database and validation
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def admin_add_doctors(request):
    form = DoctorForm
    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor added successfully.')
            return HttpResponseRedirect('/admin_view_doctors')

    context = {'form': form}
    return render(request,'admin_add_doctors.html', context)

#View for updating existing doctors and validation
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def update_doctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    form = DoctorForm(instance=doctor)
    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor updated successfully.')
            return HttpResponseRedirect('/admin_view_doctors')
    context = {'form': form}
    return render(request,'admin_add_doctors.html', context)


#View for viewing all the user reports.
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def admin_view_reports(request):
    reports = Report.objects.all
    return render(request,'admin_view_reports.html', {'reports':reports})


#View for removing the selected data from the database.
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def delete_report(request, pk):
    reports = Report.objects.get(pk=pk)
    reports.delete()
    messages.warning(request, 'Report deleted.')
    return redirect('admin_view_reports')


#View for adding reports to the database and validation
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def admin_add_reports(request):
    appointment = Appointment.objects.all
    form = ReportForm
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report added successfully.')
            return HttpResponseRedirect('/admin_view_reports')
        
    context = {'form': form, 'appointment': appointment}
    return render(request,'admin_add_reports.html', context)
   
#View for updating the selected report and validation.
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def update_report(request, pk):
    report = Report.objects.get(id=pk)
    form = ReportForm(instance=report)
    if request.method == "POST":
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated.')
            return HttpResponseRedirect('/admin_view_reports')
    context = {'form': form}
    return render(request,'admin_add_reports.html', context)


#View for seeing all the users
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def admin_view_users(request):
    patientUsers = PatientUser.objects.all
    return render(request,'admin_view_users.html', {'patientUser':patientUsers})

#View for removing the selected users from the database
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def delete_patientUser(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    messages.warning(request, 'User has been removed.')
    return redirect('admin_view_users')

#View for seeing all the services
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def admin_view_services(request):
    services = Service.objects.all
    return render(request,'admin_view_services.html',  {'services':services})


#View for adding service to the database and validation
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def admin_add_services(request):
    form = ServiceForm
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully.')
            return HttpResponseRedirect('/admin_view_services')
        

    return render(request,'admin_add_services.html', {'form':form})

#View for updating service in the database and validation
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def update_service(request, pk):
    services = Service.objects.get(id=pk)
    form = ServiceForm(instance=services)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=services)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated.')
            return HttpResponseRedirect('/admin_view_services')
    context = {'form': form}
    return render(request,'admin_add_services.html', context)


#View for deleting the selected service
@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def delete_service(request, pk):
    services = Service.objects.get(pk=pk)
    services.delete()
    messages.warning(request, 'Service removed.')
    return redirect('admin_view_services')

