from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Booking, dept, doctor
from .recommendation import find_specializations, recommend_doctors


class DoctorRecommendationTests(TestCase):
    def setUp(self):
        dermatology = dept.objects.create(
            dept_name="Dermatology",
            dept_desc="Skin care",
        )
        cardiology = dept.objects.create(
            dept_name="Cardiology",
            dept_desc="Heart care",
        )
        self.dermatologist = doctor.objects.create(
            doctor_name="Dr. Skin",
            specialization="Dermatologist",
            dept_name=dermatology,
            doctor_desc="",
        )
        doctor.objects.create(
            doctor_name="Dr. Heart",
            specialization="Cardiologist",
            dept_name=cardiology,
            doctor_desc="",
        )

    def test_find_specializations_is_case_insensitive(self):
        self.assertEqual(
            find_specializations("I have a skin rash and itching"),
            ["Dermatologist", "Skin Specialist"],
        )

    def test_recommend_doctors_matches_existing_model_fields(self):
        self.assertQuerySetEqual(
            recommend_doctors("I have a skin rash and itching"),
            [self.dermatologist],
        )

    def test_unknown_symptoms_return_no_doctors(self):
        self.assertFalse(recommend_doctors("unrecognized symptom").exists())


class PatientDashboardTests(TestCase):
    def test_dashboard_renders_appointment_status(self):
        user = User.objects.create_user(
            username="patient",
            email="patient@example.com",
            password="password",
        )
        department = dept.objects.create(
            dept_name="Cardiology",
            dept_desc="Heart care",
        )
        assigned_doctor = doctor.objects.create(
            doctor_name="Dr. Heart",
            specialization="Cardiologist",
            dept_name=department,
            doctor_desc="",
        )
        Booking.objects.create(
            patient_name="Patient",
            patient_email=user.email,
            patient_phone="1234567890",
            doctor_name=assigned_doctor,
            booking_ON=timezone.localdate(),
        )
        self.client.force_login(user)

        response = self.client.get(reverse("patient_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Recent Appointment History")
        self.assertContains(response, "Pending")
        self.assertEqual(response.context["total_appointments"], 1)
        self.assertEqual(response.context["upcoming_appointments"], 1)
