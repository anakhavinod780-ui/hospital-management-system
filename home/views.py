
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from django.template import context
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.views import LoginView

from .recommendation import recommend_doctors, find_specializations
from .forms import BookingForm, PatientSignupForm, contactform
from .models import Booking,dept, doctor


# Create your views here.
from django.shortcuts import redirect

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('index')
    return redirect('login')
def index(request):
    return render(request, 'index.html')
def about(request):
    fruits={
        'fruit':["Mango","Kiwi","Apple","Banana","Grape"]
    }
    return render(request,'about.html',fruits)
def doctors(request):
    doctors=doctor.objects.all()
    return render(request,'doctors.html',{'doctors':doctors})

def contact(request):
    if request.method == "POST":
        form = contactform(request.POST)

        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = contactform()

    return render(request, 'contact.html', {"form": form})

def departments(request):
    department = dept.objects.all()
    return render(request,'departments.html',{'department':department})
@login_required
def booking(request):

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            appointment = form.save(commit=False)

            appointment.user = request.user

            appointment.save()

            return redirect('patient_dashboard')

    else:
        form = BookingForm()

    return render(
        request,
        "bookings.html",
        {"form": form}
    )
        
def signup(request):

    if request.method == "POST":
        form = PatientSignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = PatientSignupForm()

    return render(
        request,
        'signup.html',
        {'form': form}
    )
    

def smart_recommendation(request):
    doctors = []
    symptoms = ""
    searched = False

    if request.method == "POST":
        symptoms = request.POST.get("symptoms", "").strip()
        searched = True

        if symptoms:
            doctors = recommend_doctors(symptoms)

    return render(
        request,
        "smart_recommendation.html",
        {
            "doctors": doctors,
            "symptoms": symptoms,
            "searched": searched,
        },
    ) 

@login_required
def patient_dashboard(request):

    today = timezone.localdate()

    # Get this patient's appointments
    appointments = Booking.objects.filter(
        Q(user=request.user) |
        Q(user__isnull=True, patient_email=request.user.email)
    ).distinct()

    total_appointments = appointments.count()

    pending_appointments = appointments.filter(
        status='Pending'
    ).count()

    confirmed_appointments = appointments.filter(
        status='Confirmed'
    ).count()

    completed_appointments = appointments.filter(
        status='Completed'
    ).count()

    cancelled_appointments = appointments.filter(
        status='Cancelled'
    ).count()

    upcoming_appointments = appointments.filter(
        booking_ON__gte=today
    ).exclude(
        status__in=['Completed', 'Cancelled']
    ).order_by('booking_ON')

    all_appointments = appointments.order_by('-booking_ON')

    context = {
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'upcoming_appointments': upcoming_appointments,
        'all_appointments': all_appointments,
    }

    return render(
        request,
        'patient_dashboard.html',
        context
    )
@login_required
def doctor_dashboard(request):
    doctor_profile = get_object_or_404(
        doctor,
        user=request.user
    )

    appointments = Booking.objects.filter(
        doctor_name=doctor_profile
    ).order_by('-booking_ON')

    context = {
        'doctor_profile': doctor_profile,
        'total': appointments.count(),
        'pending': appointments.filter(status='Pending').count(),
        'confirmed': appointments.filter(status='Confirmed').count(),
        'completed': appointments.filter(status='Completed').count(),
        'cancelled': appointments.filter(status='Cancelled').count(),
    }

    return render(request, 'doctor_dashboard.html', context)


@login_required
def doctor_appointments_api(request):
    doctor_profile = get_object_or_404(
        doctor,
        user=request.user
    )

    appointments = Booking.objects.filter(
        doctor_name=doctor_profile
    ).order_by('-booking_ON')

    data = [
        {
            'id': appointment.id,
            'patient_name': appointment.patient_name,
            'patient_email': appointment.patient_email,
            'patient_phone': appointment.patient_phone,
            'booking_ON': appointment.booking_ON.strftime('%d-%m-%Y'),
            'status': appointment.status,
        }
        for appointment in appointments
    ]

    return JsonResponse({
        'appointments': data,
        'total': appointments.count(),
        'pending': appointments.filter(status='Pending').count(),
        'confirmed': appointments.filter(status='Confirmed').count(),
        'completed': appointments.filter(status='Completed').count(),
        'cancelled': appointments.filter(status='Cancelled').count(),
    })


@login_required
@require_POST
def approve_appointment(request, appointment_id):
    doctor_profile = get_object_or_404(
        doctor,
        user=request.user
    )

    appointment = get_object_or_404(
        Booking,
        id=appointment_id,
        doctor_name=doctor_profile
    )

    appointment.status = 'Confirmed'
    appointment.save(update_fields=['status'])

    return JsonResponse({
        'success': True,
        'message': 'Appointment approved successfully.'
    })


@login_required
@require_POST
def cancel_appointment(request, appointment_id):
    doctor_profile = get_object_or_404(
        doctor,
        user=request.user
    )

    appointment = get_object_or_404(
        Booking,
        id=appointment_id,
        doctor_name=doctor_profile
    )

    appointment.status = 'Cancelled'
    appointment.save(update_fields=['status'])

    return JsonResponse({
        'success': True,
        'message': 'Appointment cancelled successfully.'
    })


@login_required
@require_POST
def delete_appointment(request, appointment_id):
    doctor_profile = get_object_or_404(
        doctor,
        user=request.user
    )

    appointment = get_object_or_404(
        Booking,
        id=appointment_id,
        doctor_name=doctor_profile
    )

    appointment.delete()

    return JsonResponse({
        'success': True,
        'message': 'Appointment deleted successfully.'
    })


@login_required
def patient_appointments_api(request):
    appointments = Booking.objects.filter(
        Q(user=request.user) |
        Q(user__isnull=True, patient_email=request.user.email)
    ).distinct().order_by('-booking_ON')

    data = [
        {
            'id': appointment.id,
            'doctor_name': appointment.doctor_name.doctor_name,
            'booking_ON': appointment.booking_ON.strftime('%d-%m-%Y'),
            'status': appointment.status,
        }
        for appointment in appointments
    ]

    return JsonResponse({
        'appointments': data
    })

class RoleBasedLoginView(LoginView):

    def get_success_url(self):
        if doctor.objects.filter(user=self.request.user).exists():
            return reverse('doctor_dashboard')

        return reverse('index')
