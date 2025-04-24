from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Customer, Employee, Candidate, Appointment, Booking, Skill, RecruitmentForm, EmployeeSkill
from datetime import date, timedelta

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('orchidea:register')
        self.login_url = reverse('orchidea:login')
        self.customer_register_url = reverse('orchidea:registerCustomer')
        self.employee_register_url = reverse('orchidea:registerEmployee')
        self.candidate_register_url = reverse('orchidea:registerCandidate')
        self.customer_home_url = reverse('orchidea:homeCustomer', args=[1])
        self.employee_home_url = reverse('orchidea:homeEmployee', args=[1])
        self.candidate_home_url = reverse('orchidea:homeCandidate', args=[1])

        # Create test users
        self.user = User.objects.create(username="testuser", email="testuser@example.com", password="password123")
        self.customer = Customer.objects.create(user_ID=self.user)
        self.employee = Employee.objects.create(user_ID=self.user, phone_number="1234567890")
        self.candidate = Candidate.objects.create(user_ID=self.user, phone_number="1234567890")

    def test_register_customer(self):
        response = self.client.post(self.customer_register_url, {
            'name': 'newcustomer',
            'email': 'newcustomer@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(email='newcustomer@example.com').exists())

    def test_register_employee(self):
        response = self.client.post(self.employee_register_url, {
            'name': 'newemployee',
            'email': 'newemployee@example.com',
            'password': 'password123',
            'phone_number': '9876543210'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(email='newemployee@example.com').exists())

    def test_register_candidate(self):
        response = self.client.post(self.candidate_register_url, {
            'name': 'newcandidate',
            'email': 'newcandidate@example.com',
            'password': 'password123',
            'phone_number': '9876543210'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(email='newcandidate@example.com').exists())

    def test_login_customer(self):
        response = self.client.post(reverse('orchidea:loginCustomer'), {
            'email': self.user.email,
            'password': self.user.password
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_login_employee(self):
        response = self.client.post(reverse('orchidea:loginEmployee'), {
            'email': self.user.email,
            'password': self.user.password
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_login_candidate(self):
        response = self.client.post(reverse('orchidea:loginCandidate'), {
            'email': self.user.email,
            'password': self.user.password
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_customer_home_access(self):
        response = self.client.get(self.customer_home_url)
        self.assertEqual(response.status_code, 200)

    def test_employee_home_access(self):
        response = self.client.get(self.employee_home_url)
        self.assertEqual(response.status_code, 200)

    def test_candidate_home_access(self):
        response = self.client.get(self.candidate_home_url)
        self.assertEqual(response.status_code, 200)

class BookingTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create test users
        self.user = User.objects.create(username="testcustomer", email="testcustomer@example.com", password="password123")
        self.customer = Customer.objects.create(user_ID=self.user)
        self.employee_user = User.objects.create(username="testemployee", email="testemployee@example.com", password="password123")
        self.employee = Employee.objects.create(user_ID=self.employee_user, phone_number="1234567890")

        # Create test appointment
        self.appointment = Appointment.objects.create(
            name="Test Appointment",
            description="Test Description",
            duration=timedelta(hours=1),
            cost=50.00
        )

        # Create test booking
        self.booking = Booking.objects.create(
            customer_ID=self.customer,
            employee_ID=self.employee,
            appointment_ID=self.appointment,
            date=date.today() + timedelta(days=1)
        )

        # URLs
        self.make_booking_url = reverse('orchidea:makeBooking', args=[self.user.id, self.appointment.id])
        self.bookings_url = reverse('orchidea:bookings', args=[self.user.id])
        self.single_booking_url = reverse('orchidea:customer-single-booking', args=[self.user.id, self.booking.id])
        self.cancel_booking_url = reverse('orchidea:cancelBooking', args=[self.user.id, self.booking.id])

    def test_make_booking(self):
        response = self.client.post(self.make_booking_url, {
            'employee': self.employee.id,
            'date': date.today() + timedelta(days=2)
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful booking
        self.assertTrue(Booking.objects.filter(customer_ID=self.customer, appointment_ID=self.appointment).exists())

    def test_delete_booking(self):
        response = self.client.post(self.cancel_booking_url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

    def test_edit_booking_date(self):
        new_date = date.today() + timedelta(days=3)
        response = self.client.post(self.single_booking_url, {
            'date': new_date
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.date, new_date)

class RecruitmentFormTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create test user and candidate
        self.user = User.objects.create(username="testcandidate", email="testcandidate@example.com", password="password123")
        self.candidate = Candidate.objects.create(user_ID=self.user)

        # Create test skills
        self.skill1 = Skill.objects.create(name="Skill 1")
        self.skill2 = Skill.objects.create(name="Skill 2")
        self.skill3 = Skill.objects.create(name="Skill 3")

        # Create test recruitment form
        self.recruitment_form = RecruitmentForm.objects.create(candidate_ID=self.candidate)
        self.recruitment_form.cand_Skills.add(self.skill1, self.skill2)

        # URLs
        self.apply_form_url = reverse('orchidea:apply-form', args=[self.user.id])
        self.withdraw_form_url = reverse('orchidea:withdrawRecruitment', args=[self.user.id, self.recruitment_form.id])

    def test_make_recruitment_form(self):
        response = self.client.post(self.apply_form_url, {
            'skills[]': [self.skill1.id, self.skill2.id, self.skill3.id]
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertTrue(RecruitmentForm.objects.filter(candidate_ID=self.candidate).exists())

    def test_withdraw_recruitment_form(self):
        response = self.client.post(self.withdraw_form_url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(RecruitmentForm.objects.filter(id=self.recruitment_form.id).exists())
        
        
class SkillTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create test user and employee
        self.user = User.objects.create(username="testemployee", email="testemployee@example.com", password="password123")
        self.employee = Employee.objects.create(user_ID=self.user, phone_number="1234567890")

        # Create test skills
        self.skill1 = Skill.objects.create(name="Skill 1")
        self.skill2 = Skill.objects.create(name="Skill 2")

        # Add a pre-existing skill to the employee
        EmployeeSkill.objects.create(employee=self.employee, skill=self.skill1)

        # URLs
        self.add_skill_url = reverse('orchidea:addSkill', args=[self.user.id])
        self.delete_skill_url = reverse('orchidea:deleteSkill', args=[self.user.id, self.skill1.id])

    def test_add_new_skill(self):
        response = self.client.post(self.add_skill_url, {
            'skill': self.skill2.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful addition
        self.assertTrue(EmployeeSkill.objects.filter(employee=self.employee, skill=self.skill2).exists())

    def test_delete_existing_skill(self):
        # Get the EmployeeSkill object for the pre-existing skill
        employee_skill = EmployeeSkill.objects.get(employee=self.employee, skill=self.skill1)

        # Delete the skill
        response = self.client.post(reverse('orchidea:deleteSkill', args=[self.user.id, employee_skill.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(EmployeeSkill.objects.filter(employee=self.employee, skill=self.skill1).exists())
