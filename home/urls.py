
from . import views
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
import django.contrib.auth.views as auth_views

urlpatterns = [
    path('', views.home_redirect, name='root'),
    path('home/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('doctors/', views.doctors, name='doctors'),
    path('contact/', views.contact, name='contact'),
    path('departments/', views.departments, name='departments'),
    path('booking/', views.booking, name='booking'),
    path(
    'login/',
    views.RoleBasedLoginView.as_view(
        template_name='login.html'
    ),
    name='login'
),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('smart_recommendation/', views.smart_recommendation, name='smart_recommendation'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
        path(
    'doctor-dashboard/',
    views.doctor_dashboard,
    name='doctor_dashboard'
),

path(
    'doctor-appointments-api/',
    views.doctor_appointments_api,
    name='doctor_appointments_api'
),

path(
    'approve-appointment/<int:appointment_id>/',
    views.approve_appointment,
    name='approve_appointment'
),
path('cancel-appointment/<int:appointment_id>/',views.cancel_appointment,name='cancel_appointment'),
path('delete-appointment/<int:appointment_id>/',views.delete_appointment, name='delete_appointment'),
path('patient-appointments-api/',views.patient_appointments_api,name='patient_appointments_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
