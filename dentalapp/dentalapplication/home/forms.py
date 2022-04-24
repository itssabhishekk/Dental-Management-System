from django import forms
from django.forms import ModelForm
from .models import Service
from .models import PatientUser
from .models import Doctor
from .models import Appointment
from .models import Report
from .models import contact
from django.contrib.auth.models import User


class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model=PatientUser
        fields=['date_of_birth','phone_number','address','profile_picture']
        

class UpdatePatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']
            
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UpdatePatientForm(forms.ModelForm):
    class Meta:
        model=PatientUser
        fields=['date_of_birth','phone_number','address','profile_picture']
        
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields =  ('patientUser', 'doctor', 'service', 'date', 'time', 'description')
        
        widgets = {
            'patientUser': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'datePickerId'}),            
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'min': '09:00:00', 'max' : '17:00:00'}),            
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }

class UserAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields =  ('doctor', 'service', 'date', 'time', 'description')

        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control','type': 'date', 'id': 'datePickerId'}),            
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'min': '09:00:00', 'max' : '17:00:00'}),          
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
 
class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields =  ('full_name', 'qualification', 'date_of_birth', 'email', 'phone_number', 'address', 'profile_picture', 'experience')

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name',}),
            'qualification': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Bachelors/Masters in Dental Science'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control','type': 'date', 'max': '2000-01-01'}),  
            'email': forms.EmailInput(attrs={'class': 'form-control','type': 'email', 'placeholder': 'example@gmail.com'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+977-mobileNumber'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street, City'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'experience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '- years'}),

        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report

        fields =  ('appointment', 'problems', 'prescription', 'other_details')
        widgets = {
            'appointment': forms.Select(attrs={'class': 'form-control'}),
            'problems': forms.Textarea(attrs={'class': 'form-control'}),
            'prescription': forms.Textarea(attrs={'class': 'form-control'}),
            'other_details': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['appointment'].queryset = Appointment.objects.filter(status=4)


    
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields =  ('service_name', 'cost', 'description')

        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),

        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = contact
        fields =  ('name', 'email', 'subject', 'phone_number', 'message')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'}),
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ""
        self.fields['email'].label = ""
        self.fields['subject'].label = ""
        self.fields['phone_number'].label = ""
        self.fields['message'].label = ""

