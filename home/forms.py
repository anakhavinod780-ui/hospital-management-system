
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, contact, PatientProfile


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'patient_name', 'patient_email', 'patient_phone',
            'doctor_name', 'booking_ON'
        ]
        labels = {
            'patient_name': 'Your Name',
            'patient_email': 'Your Email',
            'patient_phone': 'Your Phone',
            'booking_ON': 'Booking Date',
            'doctor_name': 'Select Doctor',
        }
        widgets = {
            'patient_name': forms.TextInput(attrs={
                'placeholder': 'Enter your name',
                'class': 'form-control'
            }),
            'patient_email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'form-control'
            }),
            'patient_phone': forms.TextInput(attrs={
                'placeholder': 'Enter your phone number',
                'class': 'form-control'
            }),
            'booking_ON': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'doctor_name': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class contactform(forms.ModelForm):
    class Meta:
        model = contact
        fields = ['name', 'email', 'phone', 'Address']
        labels = {
            'name': 'Name',
            'email': 'Email',
            'phone': 'Phone',
            'Address': 'Address'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Enter your phone number',
                'class': 'form-control'
            }),
            'Address': forms.Textarea(attrs={
                'placeholder': 'Enter your address',
                'class': 'form-control'
            }),
        }


class PatientSignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['full_name', 'phone', 'address', 'profile_picture']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control'
            }),
        }
