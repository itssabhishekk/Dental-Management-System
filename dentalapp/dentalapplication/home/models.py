from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User

# Create your models here.
class Service(models.Model):
    service_name = models.CharField('Service',max_length=50)
    cost = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.service_name

class Doctor(models.Model):
    full_name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pic/doctor_profile_pic/',null=True,blank=True)
    experience = models.CharField(max_length=10, default="1 year")

    def __str__(self):
        return self.full_name

class PatientUser(models.Model):
    user=models.OneToOneField(User, null=True, blank=False,on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pic/user_profile_pic/', default='img/defaultuser.png')

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name


class Appointment(models.Model):
    patientUser = models.ForeignKey(PatientUser, blank=False, null=False, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, blank=False, null=False, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, blank=False, null=False, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    status = models.IntegerField('Status', default=0)
    
    def __str__(self):
        return self.patientUser.user.first_name+" "+self.patientUser.user.last_name+"  ("+str(self.date)+")  ("+str(self.time)+")"



class Report(models.Model):
    appointment = models.ForeignKey(Appointment, blank=False, null=False, on_delete=models.CASCADE)
    problems = models.TextField()
    prescription = models.TextField()
    other_details = models.TextField()
    
    def __str__(self):
        return self.appointment.patientUser.user.first_name+" "+self.appointment.patientUser.user.last_name+"  ("+str(self.appointment.date)+")  ("+str(self.appointment.time)+")"


