from . import views
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
import django.contrib.auth.views as auth_views
urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('doctors/',views.doctors,name='doctors'),
    path('contact/',views.contact,name='contact'),
    path('departments/',views.departments,name='departments'),
    path('booking/',views.booking,name='booking'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/',views.signup,name='signup'),
    path('smart_recommendation/', views.smart_recommendation, name='smart_recommendation'),
    path(
    'patient-dashboard/',
    views.patient_dashboard,
    name='patient_dashboard'
),

path(
    'my-profile/',
    views.my_profile,
    name='my_profile'
),

path(
    'edit-profile/',
    views.edit_profile,
    name='edit_profile'
),

path(
    'delete-account/',
    views.delete_account,
    name='delete_account'
),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
