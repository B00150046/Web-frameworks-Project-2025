from django.test import TestCase, Client
from django.urls import reverse
from orchidea.models import User, Customer, Employee, Candidate, Appointment, Booking, Skill, RecruitmentForm, EmployeeSkill
from datetime import date, timedelta
from unittest.mock import patch

class BaseTestCase(TestCase):
    fixtures = ['sample_data.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def force_login_with_mock(self, user):
        """Manually log in the user without updating last_login."""
        session = self.client.session
        session["_auth_user_id"] = user.pk
        session["_auth_user_backend"] = "django.contrib.auth.backends.ModelBackend"
        session.save()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                        CUSTOMER-SPECIFIC TESTS                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
class CustomerTests(BaseTestCase):
    def test_customer_login(self):
        response = self.client.post(reverse('orchidea:loginCustomer'), {
            'email': "Cust1@Cust1.com",
            'password': "password"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orchidea:homeCustomer', args=[1]))

    def test_customer_register(self):
        response = self.client.post(reverse('orchidea:registerCustomer'), {
            'name': 'new_customer',
            'email': 'new_customer@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302, "Expected redirect after successful registration.")
        self.assertTrue(User.objects.filter(email='new_customer@example.com').exists())

    def test_customer_book_appointment(self):
        customer = Customer.objects.get(user_ID__username="Customer1")
        employee = Employee.objects.get(user_ID__username="Employee1")
        appointment = Appointment.objects.filter(name="Detoxifying Body Wrap").first()
        self.assertIsNotNone(appointment)

        session = self.client.session
        session["customer_id"] = customer.user_ID.id
        session["user_name"] = customer.user_ID.username
        session.save()

        response = self.client.post(reverse('orchidea:makeBooking', args=[customer.user_ID.id, appointment.id]), {
            'employee': employee.id,
            'date': date.today() + timedelta(days=2)
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Booking.objects.filter(customer_ID=customer, appointment_ID=appointment).exists())

    def test_customer_cancel_booking(self):
        customer = Customer.objects.get(user_ID__username="Customer1")
        booking = Booking.objects.filter(customer_ID=customer).first()

        if not booking:
            employee = Employee.objects.get(user_ID__username="Employee1")
            appointment = Appointment.objects.filter(name="Detoxifying Body Wrap").first()
            self.assertIsNotNone(appointment, "Appointment 'Detoxifying Body Wrap' does not exist.")
            booking = Booking.objects.create(
                customer_ID=customer,
                employee_ID=employee,
                appointment_ID=appointment,
                date=date.today() + timedelta(days=1)
            )

        self.assertIsNotNone(booking, "Booking does not exist for the customer.")

        session = self.client.session
        session["customer_id"] = customer.user_ID.id
        session["user_name"] = customer.user_ID.username
        session.save()

        response = self.client.post(reverse('orchidea:cancelBooking', args=[customer.user_ID.id, booking.id]))
        self.assertEqual(response.status_code, 302, "Expected redirect after successful booking cancellation.")
        self.assertFalse(Booking.objects.filter(id=booking.id).exists())

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                        EMPLOYEE-SPECIFIC TESTS                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
class EmployeeTests(BaseTestCase):
    def test_employee_login(self):
        response = self.client.post(reverse('orchidea:loginEmployee'), {
            'email': "Emp1@Emp1.com",
            'password': "password"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orchidea:homeEmployee', args=[2]))

    def test_employee_register(self):
        response = self.client.post(reverse('orchidea:registerEmployee'), {
            'name': 'new_employee',
            'email': 'new_employee@example.com',
            'password': 'password123',
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='new_employee@example.com').exists())

    def test_employee_add_skill(self):
        employee = Employee.objects.get(user_ID__username="Employee1")
        skill = Skill.objects.get(name="Wellness and Nutrition Coaching")

        session = self.client.session
        session["employee_id"] = employee.user_ID.id
        session["user_name"] = employee.user_ID.username
        session.save()

        response = self.client.post(reverse('orchidea:addSkill', args=[employee.user_ID.id]), {
            'skill': skill.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(EmployeeSkill.objects.filter(employee=employee, skill=skill).exists())

    def test_employee_delete_skill(self):
        employee = Employee.objects.get(user_ID__username="Employee1")
        employee_skill = EmployeeSkill.objects.filter(employee=employee, skill__name="Massage Therapy").first()
        self.assertIsNotNone(employee_skill)

        session = self.client.session
        session["employee_id"] = employee.user_ID.id
        session["user_name"] = employee.user_ID.username
        session.save()

        response = self.client.post(reverse('orchidea:deleteSkill', args=[employee.user_ID.id, employee_skill.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(EmployeeSkill.objects.filter(id=employee_skill.id).exists())

    def test_employee_cancel_booking(self):
        employee = Employee.objects.get(user_ID__username="Employee1")
        booking = Booking.objects.filter(employee_ID=employee).first()

        if not booking:
            customer = Customer.objects.get(user_ID__username="Customer1")
            appointment = Appointment.objects.filter(name="Detoxifying Body Wrap").first()
            booking = Booking.objects.create(
                customer_ID=customer,
                employee_ID=employee,
                appointment_ID=appointment,
                date=date.today() + timedelta(days=1)
            )

        session = self.client.session
        session["employee_id"] = employee.user_ID.id
        session["user_name"] = employee.user_ID.username
        session.save()

        response = self.client.post(reverse('orchidea:cancelEmployeeBooking', args=[employee.user_ID.id, booking.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Booking.objects.filter(id=booking.id).exists())

    def test_employee_view_forms(self):
        employee = Employee.objects.get(user_ID__username="Employee1")

        session = self.client.session
        session["employee_id"] = employee.user_ID.id
        session["user_name"] = employee.user_ID.username
        session.save()

        self.force_login_with_mock(employee.user_ID)

        response = self.client.get(reverse('orchidea:employee-recruitment', args=[employee.user_ID.id]))
        self.assertEqual(response.status_code, 200, "Expected successful response for viewing recruitment forms.")
        self.assertContains(response, "Recruitment Forms")

    def test_employee_accept_form(self):
        employee = Employee.objects.get(user_ID__username="Employee1")
        recruitment_form = RecruitmentForm.objects.first()
        self.assertIsNotNone(recruitment_form, "Expected at least one recruitment form to exist.")
        self.force_login_with_mock(employee.user_ID)

        candidate_id = recruitment_form.candidate_ID.id

        response = self.client.post(reverse('orchidea:acceptRecruitment', args=[employee.user_ID.id, recruitment_form.id]))
        self.assertEqual(response.status_code, 302)

        accepted_form = RecruitmentForm.objects.filter(id=recruitment_form.id).first()
        if accepted_form:
            self.assertEqual(accepted_form.status, "Accepted")
        else:
            candidate_exists = Candidate.objects.filter(id=candidate_id).exists()
            self.assertFalse(candidate_exists, "Candidate should be deleted after accepting the recruitment form.")

    def test_employee_deny_form(self):
        employee = Employee.objects.get(user_ID__username="Employee1")
        recruitment_form = RecruitmentForm.objects.first()
        self.assertIsNotNone(recruitment_form, "Expected at least one recruitment form to exist.")

        session = self.client.session
        session["employee_id"] = employee.user_ID.id
        session["user_name"] = employee.user_ID.username
        session.save()

        self.force_login_with_mock(employee.user_ID)

        response = self.client.post(reverse('orchidea:rejectRecruitment', args=[employee.user_ID.id, recruitment_form.id]))
        self.assertEqual(response.status_code, 302, "Expected redirect after denying a recruitment form.")
        self.assertFalse(RecruitmentForm.objects.filter(id=recruitment_form.id).exists())

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                        CANDIDATE-SPECIFIC TESTS                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
class CandidateTests(BaseTestCase):
    def test_candidate_login(self):
        response = self.client.post(reverse('orchidea:loginCandidate'), {
            'email': "Cand1@Cand1.com",
            'password': "password"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orchidea:homeCandidate', args=[3]))

    def test_candidate_register(self):
        response = self.client.post(reverse('orchidea:registerCandidate'), {
            'name': 'new_candidate',
            'email': 'new_candidate@example.com',
            'password': 'password123',
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='new_candidate@example.com').exists())

    def test_candidate_submit_form(self):
        candidate = Candidate.objects.get(user_ID__username="Candidate1")

        session = self.client.session
        session["candidate_id"] = candidate.user_ID.id
        session["user_name"] = candidate.user_ID.username
        session.save()

        response = self.client.post(reverse('orchidea:apply-form', args=[candidate.user_ID.id]), {
            'skills[]': [1, 2, 3]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(RecruitmentForm.objects.filter(candidate_ID=candidate).exists())

    def test_candidate_withdraw_form(self):
        candidate = Candidate.objects.get(user_ID__username="Candidate1")
        recruitment_form = RecruitmentForm.objects.get(candidate_ID=candidate)

        session = self.client.session
        session["candidate_id"] = candidate.user_ID.id
        session["user_name"] = candidate.user_ID.username
        session.save()

        response = self.client.post(reverse('orchidea:withdrawRecruitment', args=[candidate.user_ID.id, recruitment_form.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(RecruitmentForm.objects.filter(id=recruitment_form.id).exists())
