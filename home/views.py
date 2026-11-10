
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .recommendation import recommend_doctors, find_specializations
from .forms import BookingForm, PatientSignupForm, contactform, PatientProfileForm
from .models import Booking, PatientProfile, dept, doctor


# Create your views here.
def index(request):
  return render(request,'index.html')
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

            user = form.save()

            PatientProfile.objects.create(
                user=user,
                full_name=user.username
            )

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

    profile, created = PatientProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.username
        }
    )

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
        'profile': profile,
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
def my_profile(request):

    profile, created = PatientProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.username
        }
    )

    return render(
        request,
        'my_profile.html',
        {'profile': profile}
    )
@login_required
def edit_profile(request):

    profile, created = PatientProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.username
        }
    )

    if request.method == 'POST':

        form = PatientProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect('my_profile')

    else:

        form = PatientProfileForm(instance=profile)

    return render(
        request,
        'edit_profile.html',
        {'form': form}
    )
@login_required
def delete_account(request):

    if request.method == 'POST':

        user = request.user

        user.delete()

        return redirect('login')

    return render(
        request,
        'delete_account.html'
    )