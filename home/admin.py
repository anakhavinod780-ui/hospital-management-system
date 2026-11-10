from django.contrib import admin
from . models import Booking, contact, dept, doctor
# Register your models here.
admin.site.register(dept)
admin.site.register(doctor)
admin.site.register(Booking)
admin.site.register(contact)