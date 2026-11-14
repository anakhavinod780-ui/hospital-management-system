from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class dept(models.Model):
    dept_name=models.CharField(max_length=100)
    dept_desc=models.TextField()
    def __str__(self):
        return self.dept_name
class doctor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    doctor_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    dept_name = models.ForeignKey(dept, on_delete=models.CASCADE)
    doctor_desc = models.TextField()
    doctors_image = models.ImageField(
        upload_to='doctors/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.doctor_name
class Booking(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=15)

    doctor_name = models.ForeignKey(
        doctor,
        on_delete=models.CASCADE
    )

    booking_ON = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Pending'
    )

    def __str__(self):
        return f"{self.patient_name} - {self.booking_ON}"

class contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    Address=models.TextField()
    def __str__(self):
        return self.name



