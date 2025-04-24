from django.test import TestCase, Client
from django.urls import reverse
from orchidea.models import User, Customer, Employee, Candidate, Appointment, Booking, Skill, RecruitmentForm, EmployeeSkill
from datetime import date, timedelta  # Ensure timedelta is imported

class BaseTestCase(TestCase):
    fixtures = ['sample_data.json']  # Use the correct fixture file name

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def custom_force_login(self, user):
        """Custom method to simulate force_login without updating last_login."""
        session = self.client.session
        session['_auth_user_id'] = user.id
        session.save()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                GENERAL TESTS                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
class GeneralTests(BaseTestCase):
    def test_home_view(self):
        response = self.client.get(reverse('orchidea:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Orchidea Lux")

    def test_register_view(self):
        response = self.client.get(reverse('orchidea:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Before we register you in, are you an...")

    def test_login_view(self):
        response = self.client.get(reverse('orchidea:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Before you login are you an...")  # Update to match the actual text in the template

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                        CUSTOMER-SPECIFIC TESTS                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
class CustomerTests(BaseTestCase):
    def test_customer_registration(self):
        response = self.client.post(reverse('orchidea:registerCustomer'), {
            'name': 'new_customer',
            'email': 'new_customer@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(email='new_customer@example.com').exists())

    def test_customer_login(self):
        response = self.client.post(reverse('orchidea:loginCustomer'), {
            'email': "customer1@example.com",
            'password': "password"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orchidea:homeCustomer', args=[1]))

    def test_customer_home_view(self):
        user = User.objects.get(username="customer1")
        self.custom_force_login(user)
        response = self.client.get(reverse('orchidea:homeCustomer', args=[user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome, customer1")

    def test_customer_appointments_view(self):
        user = User.objects.get(username="customer1")
        self.custom_force_login(user)
        response = self.client.get(reverse('orchidea:appointments', args=[user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Appointments")

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                        EMPLOYEE-SPECIFIC TESTS                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
class EmployeeTests(BaseTestCase):
    def test_employee_registration(self):
        response = self.client.post(reverse('orchidea:registerEmployee'), {
            'name': 'new_employee',
            'email': 'new_employee@example.com',
            'password': 'password123',
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(email='new_employee@example.com').exists())

    def test_employee_login(self):
        response = self.client.post(reverse('orchidea:loginEmployee'), {
            'email': "employee1@example.com",
            'password': "password"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orchidea:homeEmployee', args=[2]))

    def test_employee_home_view(self):
        user = User.objects.get(username="employee1")
        self.custom_force_login(user)
        response = self.client.get(reverse('orchidea:homeEmployee', args=[user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome, employee1")

    def test_employee_manage_bookings_view(self):
        user = User.objects.get(username="employee1")
        self.custom_force_login(user)
        response = self.client.get(reverse('orchidea:employee-bookings', args=[user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manage Appointments")  # Updated to match the actual text in the template

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                        CANDIDATE-SPECIFIC TESTS                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
class CandidateTests(BaseTestCase):
    def test_candidate_registration(self):
        response = self.client.post(reverse('orchidea:registerCandidate'), {
            'name': 'new_candidate',
            'email': 'new_candidate@example.com',
            'password': 'password123',
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(email='new_candidate@example.com').exists())

    def test_candidate_login(self):
        response = self.client.post(reverse('orchidea:loginCandidate'), {
            'email': "candidate1@example.com",
            'password': "password"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orchidea:homeCandidate', args=[3]))

    def test_candidate_home_view(self):
        user = User.objects.get(username="candidate1")
        self.custom_force_login(user)
        response = self.client.get(reverse('orchidea:homeCandidate', args=[user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome, candidate1")

    def test_candidate_apply_form_view(self):
        user = User.objects.get(username="candidate1")
        self.custom_force_login(user)
        response = self.client.get(reverse('orchidea:apply-form', args=[user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apply for Recruitment")

    def test_candidate_submit_recruitment_form(self):
        user = User.objects.get(username="candidate1")
        self.custom_force_login(user)
        response = self.client.post(reverse('orchidea:apply-form', args=[user.id]), {
            'skills[]': [1, 2, 3]
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
        self.assertTrue(RecruitmentForm.objects.filter(candidate_ID__user_ID=user).exists())

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                        BOOKING-SPECIFIC TESTS                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
class BookingTests(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.customer = Customer.objects.get(user_ID__username="customer1")
        cls.employee = Employee.objects.get(user_ID__username="employee1")
        cls.appointment = Appointment.objects.create(
            name="Test Appointment",
            description="Test Description",
            duration=timedelta(hours=1),  # Use a valid timedelta object
            cost="100.00"
        )
        cls.booking = Booking.objects.create(
            customer_ID=cls.customer,
            employee_ID=cls.employee,
            appointment_ID=cls.appointment,
            date=date.today() + timedelta(days=1)
        )
        cls.cancel_booking_url = reverse('orchidea:cancelBooking', args=[cls.employee.user_ID.id, cls.booking.id])  # Use employee's User_Id

    def test_make_booking(self):
        response = self.client.post(reverse('orchidea:makeBooking', args=[self.customer.user_ID.id, self.appointment.id]), {
            'employee': self.employee.id,
            'date': date.today() + timedelta(days=2)
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Booking.objects.filter(customer_ID=self.customer, appointment_ID=self.appointment).exists())

    def test_customer_delete_booking(self):
        self.custom_force_login(self.customer.user_ID)  # Use custom method
        response = self.client.post(self.cancel_booking_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

    def test_employee_delete_booking(self):
        self.custom_force_login(self.employee.user_ID)  # Ensure the employee is logged in
        response = self.client.post(self.cancel_booking_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

class RecruitmentFormTests(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.candidate = Candidate.objects.get(user_ID__username="candidate1")
        cls.skill1 = Skill.objects.get(name="Skill 1")
        cls.skill2 = Skill.objects.get(name="Skill 2")
        cls.skill3 = Skill.objects.get(name="Skill 3")
        cls.recruitment_form = RecruitmentForm.objects.create(candidate_ID=cls.candidate)
        cls.recruitment_form.cand_Skills.add(cls.skill1, cls.skill2)

    def test_make_recruitment_form(self):
        response = self.client.post(reverse('orchidea:apply-form', args=[self.candidate.user_ID.id]), {
            'skills[]': [self.skill1.id, self.skill2.id, self.skill3.id]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(RecruitmentForm.objects.filter(candidate_ID=self.candidate).exists())

    def test_withdraw_recruitment_form(self):
        response = self.client.post(reverse('orchidea:withdrawRecruitment', args=[self.candidate.user_ID.id, self.recruitment_form.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(RecruitmentForm.objects.filter(id=self.recruitment_form.id).exists())

