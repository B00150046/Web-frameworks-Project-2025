from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Customer, Employee, Candidate, Appointment, Booking, Skill, RecruitmentForm, EmployeeSkill
from datetime import date, timedelta  # Ensure timedelta is imported

class BaseTestCase(TestCase):
    fixtures = ['orchidea/fixtures/sample_data.json']  # Ensure the correct path to the fixture

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def custom_force_login(self, user):
        """Custom method to simulate force_login without updating last_login."""
        session = self.client.session
        session['_auth_user_id'] = user.id
        session.save()

class UserTests(BaseTestCase):
    def test_login_customer(self):
        response = self.client.post(reverse('orchidea:loginCustomer'), {
            'email': "customer1@example.com",
            'password': "password"  # Plain text password corresponding to the hashed password
        })
        if response.status_code != 302:
            print(response.content.decode())  # Debugging: Print the response content
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orchidea:homeCustomer', args=[1]))

    def test_login_employee(self):
        response = self.client.post(reverse('orchidea:loginEmployee'), {
            'email': "employee1@example.com",
            'password': "password"  # Ensure this matches the plain text password
        })
        if response.status_code != 302:
            print(response.content.decode())  # Debugging: Print the response content
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orchidea:homeEmployee', args=[2]))

    def test_login_candidate(self):
        response = self.client.post(reverse('orchidea:loginCandidate'), {
            'email': "candidate1@example.com",
            'password': "password"  # Ensure this matches the plain text password
        })
        if response.status_code != 302:
            print(response.content.decode())  # Debugging: Print the response content
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orchidea:homeCandidate', args=[3]))

    def test_invalid_login(self):
        response = self.client.post(reverse('orchidea:loginCustomer'), {
            'email': "invalid@example.com",
            'password': "wrongpassword"
        })
        if response.status_code != 200:
            print(response.content.decode())  # Debugging: Print the response content
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password")

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

