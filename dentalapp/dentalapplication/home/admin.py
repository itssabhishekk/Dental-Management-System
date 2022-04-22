from django.contrib import admin
from .models import Service
from .models import Doctor
from .models import PatientUser
from .models import Appointment 
from .models import Report 
from .models import contact 



from .models import PatientUser

# Register your models here.
admin.site.register(Service)
admin.site.register(Doctor)
admin.site.register(PatientUser)
admin.site.register(Appointment)
admin.site.register(Report)
admin.site.register(contact)
