from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import UserProfile, doctors, dpt

# Create your tests here.
class BookingViewTests(TestCase):
	def test_get_renders_empty_booking_form(self):
		response = self.client.get("/booking/")
		self.assertEqual(response.status_code, 200)
		self.assertFalse(response.context["form"].is_bound)

	def test_invalid_post_renders_bound_form_with_errors(self):
		response = self.client.post("/booking/", data={})

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context["form"].is_bound)
		self.assertIn("patient_name", response.context["form"].errors)

	def test_booking_prefills_profile_and_selected_doctor(self):
		user = User.objects.create_user(
			username="patient1",
			password="test-password",
			first_name="Asha",
			last_name="Kumar",
			email="asha@example.com",
		)
		UserProfile.objects.create(user=user, phone="9876543210")
		department = dpt.objects.create(
			department_name="Dermatology",
			dpt_description="Skin care",
		)
		selected_doctor = doctors.objects.create(
			doctor_name="Anjali Raj",
			doctor_specialization="Dermatologist",
			department_name=department,
		)

		self.client.force_login(user)
		response = self.client.get(
			f"/booking/?doctor={selected_doctor.id}"
		)
		form = response.context["form"]

		self.assertEqual(form.initial["patient_name"], "Asha Kumar")
		self.assertEqual(form.initial["patient_email"], "asha@example.com")
		self.assertEqual(form.initial["patient_phone"], "9876543210")
		self.assertEqual(form.initial["doctor_name"], selected_doctor)
		self.assertEqual(form.initial["booked_on"], timezone.localdate())
