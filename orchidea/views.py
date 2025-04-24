from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from .models import User, Customer, Employee, Appointment, Skill, Candidate, RecruitmentForm, Booking, EmployeeSkill, CandidateSkill
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger('orchidea')

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                GENERAL VIEWS                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
class HomeView(generic.View):
    def get(self, request):
        return render(request, 'orchidea/Home.html')

class RegisterView(generic.View):
    template_name = 'orchidea/Register/Register.html'

    def get(self, request):
        return render(request, self.template_name)

class LoginView(generic.View):
    template_name = 'orchidea/Login/Login.html'

    def get(self, request):
        return render(request, self.template_name)

class LogoutView(generic.View):
    template_name = 'orchidea/Login/Logout.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        request.session.flush()
        return redirect('orchidea:home')

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                        CUSTOMER-SPECIFIC VIEWS                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
class CustRegisterView(generic.View):
    template_name = 'orchidea/Register/Cust-Register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not email or not password:
            return render(request, self.template_name, {"error": "All fields are required"})

        if User.objects.filter(email=email).exists():
            return render(request, self.template_name, {"error": "Email already registered"})

        try:
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password)
            )
            customer = Customer.objects.create(user_ID=user)
            request.session["customer_id"] = customer.id
            request.session["user_name"] = user.username
            return redirect("orchidea:homeCustomer", User_Id=user.id)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return render(request, self.template_name, {"error": "An error occurred during registration. Please try again."})

class LoginCustomerView(generic.View):
    template_name = 'orchidea/Login/Login-Cust.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            if not check_password(password, user.password):
                return render(request, self.template_name, {"error": "Invalid email or password"})
            customer = Customer.objects.get(user_ID=user)
            request.session["customer_id"] = customer.id
            request.session["user_name"] = user.username
            return redirect("orchidea:homeCustomer", User_Id=user.id)
        except User.DoesNotExist:
            return render(request, self.template_name, {"error": "Invalid email or password"})
        except Customer.DoesNotExist:
            return render(request, self.template_name, {"error": "No customer account linked to this user"})

class CustomerHomeView(generic.View):
    template_name = 'orchidea/Customer/Customer-Home.html'

    def get(self, request, User_Id):
        if request.session.get("customer_id") != User_Id:
            return HttpResponse("You are not authorized to view this page.", status=403)
        user = get_object_or_404(User, id=User_Id)
        customer = get_object_or_404(Customer, user_ID=user)
        return render(request, self.template_name, {
            'customer': customer,
            'user_type': 'customer',
            'User_Id': User_Id
        })

class AppointmentView(generic.View):
    template_name = 'orchidea/Customer/Appointments/Appointments.html'

    def get(self, request, User_Id):
        user = get_object_or_404(User, id=User_Id)
        appointments = Appointment.objects.all()
        return render(request, self.template_name, {
            'user': user,
            'appointments': appointments,
            'user_type': 'customer',
            'User_Id': User_Id
        })

class SingleAppointmentView(generic.View):
    template_name = 'orchidea/Customer/Appointments/AppointmentDetail.html'

    def get(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        appointment = get_object_or_404(Appointment, id=pk)
        return render(request, self.template_name, {
            'user': user,
            'appointment': appointment,
            'user_type': 'customer',
            'User_Id': User_Id
        })

class makeBookingView(generic.View):
    template_name = 'orchidea/Customer/Appointments/makeBooking.html'

    def get(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        customer = get_object_or_404(Customer, user_ID=user)
        appointment = get_object_or_404(Appointment, id=pk)
        employees = Employee.objects.all()
        return render(request, self.template_name, {
            'customer': customer,
            'appointment': appointment,
            'employees': employees,
            'user_type': 'customer',
            'User_Id': User_Id
        })

    def post(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        customer = get_object_or_404(Customer, user_ID=user)
        employee_id = request.POST.get('employee')
        appointment = get_object_or_404(Appointment, id=pk)
        date = request.POST.get('date')

        if not employee_id or not date:
            return render(request, self.template_name, {
                'customer': customer,
                'appointment': appointment,
                'employees': Employee.objects.all(),
                'error': 'Please select an employee and a date.',
                'user_type': 'customer',
                'User_Id': User_Id
            })

        employee = get_object_or_404(Employee, id=employee_id)
        Booking.objects.create(
            customer_ID=customer,
            appointment_ID=appointment,
            employee_ID=employee,
            date=date
        )
        return redirect('orchidea:bookings', User_Id=User_Id)

class BookingView(generic.View):
    template_name = 'orchidea/Customer/Bookings/Bookings.html'

    def get(self, request, User_Id):
        user = get_object_or_404(User, id=User_Id)
        customer = get_object_or_404(Customer, user_ID=user)
        bookings = Booking.objects.filter(customer_ID=customer)
        return render(request, self.template_name, {
            'user': user,
            'customer': customer,
            'bookings': bookings,
            'user_type': 'customer',
            'User_Id': User_Id
        })

    def post(self, request, User_Id, pk=None):
        if pk:
            booking = get_object_or_404(Booking, id=pk)
            booking.delete()
            return redirect('orchidea:bookings', User_Id=User_Id)
        return HttpResponse(status=405)

class SingleBookingViewDetail(generic.View):
    template_name = 'orchidea/Customer/Bookings/Booking-Detail.html'

    def get(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        customer = get_object_or_404(Customer, user_ID=user)
        booking = get_object_or_404(Booking, id=pk, customer_ID=customer)
        return render(request, self.template_name, {
            'user': user,
            'customer': customer,
            'booking': booking,
            'user_type': 'customer',
            'User_Id': User_Id
        })

    def post(self, request, User_Id, pk):
        booking = get_object_or_404(Booking, id=pk)
        new_date = request.POST.get('date')

        if not new_date:
            return render(request, self.template_name, {
                'user': request.user,
                'customer': booking.customer_ID,
                'booking': booking,
                'error': 'Please provide a valid date.',
                'User_Id': User_Id
            })

        booking.date = new_date
        booking.save()
        return redirect('orchidea:customer-single-booking', User_Id=User_Id, pk=pk)

class CancelBookingView(generic.View):
    template_name = 'orchidea/Customer/Bookings/Delete-Booking.html'

    def get(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        customer = get_object_or_404(Customer, user_ID=user)
        booking = get_object_or_404(Booking, id=pk, customer_ID=customer)
        return render(request, self.template_name, {
            'user': user,
            'customer': customer,
            'booking': booking,
            'User_Id': User_Id
        })

    def post(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        customer = get_object_or_404(Customer, user_ID=user)
        booking = get_object_or_404(Booking, id=pk, customer_ID=customer)
        booking.delete()  # Delete the booking
        return redirect('orchidea:bookings', User_Id=User_Id)  # Redirect to the bookings page

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                        EMPLOYEE-SPECIFIC VIEWS                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
class EmpRegisterView(generic.View):
    template_name = 'orchidea/Register/Emp-Register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")

        if not username or not email or not password or not phone_number:
            return render(request, self.template_name, {"error": "All fields are required"})

        if User.objects.filter(email=email).exists():
            return render(request, self.template_name, {"error": "Email already registered"})

        try:
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password)
            )
            employee = Employee.objects.create(user_ID=user, phone_number=phone_number)
            request.session["employee_id"] = employee.id
            request.session["user_name"] = user.username
            return redirect("orchidea:homeEmployee", User_Id=user.id)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return render(request, self.template_name, {"error": "An error occurred during registration. Please try again."})

class LoginEmployeeView(generic.View):
    template_name = 'orchidea/Login/Login-Emp.html'

    def get(self, request):
        logger.debug("Employee login page accessed.")
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            logger.debug(f"Attempting login for employee with email: {email}")
            user = User.objects.get(email=email)
            if not check_password(password, user.password):
                logger.warning(f"Password mismatch for employee email: {email}")
                return render(request, self.template_name, {"error": "Invalid email or password"})
            employee = Employee.objects.get(user_ID=user)
            logger.info(f"Employee login successful: {employee.user_ID.username}")
            request.session["employee_id"] = employee.id
            request.session["user_name"] = user.username
            return redirect("orchidea:homeEmployee", User_Id=user.id)
        except User.DoesNotExist:
            logger.error(f"User not found for email: {email}")
            return render(request, self.template_name, {"error": "Invalid email or password"})
        except Employee.DoesNotExist:
            logger.error(f"No employee account linked to email: {email}")
            return render(request, self.template_name, {"error": "No employee account linked to this user"})
        except Exception as e:
            logger.critical(f"Unexpected error during employee login: {e}")
            return render(request, self.template_name, {"error": "An unexpected error occurred. Please try again."})

class HomeEmployeeView(generic.View):
    template_name = 'orchidea/Employee/Employee-Home.html'

    def get(self, request, User_Id):
        user = get_object_or_404(User, id=User_Id)
        employee = get_object_or_404(Employee, user_ID=user)
        return render(request, self.template_name, {
            'employee': employee,
            'user_type': 'employee',
            'User_Id': User_Id
        })

class EmployeeBookingView(generic.View):
    template_name = 'orchidea/Employee/BookingManagement/manageBookings.html'

    def get(self, request, User_Id):
        user = get_object_or_404(User, id=User_Id)
        employee = get_object_or_404(Employee, user_ID=user)
        bookings = Booking.objects.filter(employee_ID=employee)
        return render(request, self.template_name, {
            'employee': employee,
            'bookings': bookings,
            'user_type': 'employee',
            'User_Id': User_Id
        })

class EmployeeBookingDetailView(generic.View):
    template_name = 'orchidea/Employee/BookingManagement/View-Booking-Detail.html'

    def get(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        employee = get_object_or_404(Employee, user_ID=user)
        booking = get_object_or_404(Booking, id=pk, employee_ID=employee)
        return render(request, self.template_name, {
            'employee': employee,
            'booking': booking,
            'user_type': 'employee',
            'User_Id': User_Id
        })

class CancelBookingView(generic.View):
    template_name = 'orchidea/Employee/BookingManagement/Cancel-Booking.html'

    def get(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        if not hasattr(user, 'employee'):
            return HttpResponse(status=403)
        try:
            employee = Employee.objects.get(user_ID=user)
        except Employee.DoesNotExist:
            return HttpResponse(status=404)
        booking = get_object_or_404(Booking, id=pk, employee_ID=employee)
        return render(request, self.template_name, {
            'employee': employee,
            'booking': booking,
            'User_Id': User_Id
        })

    def post(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        if not hasattr(user, 'employee'):
            return HttpResponse(status=403)
        try:
            employee = Employee.objects.get(user_ID=user)
        except Employee.DoesNotExist:
            return HttpResponse(status=404)
        booking = get_object_or_404(Booking, id=pk, employee_ID=employee)
        booking.delete()
        return redirect('orchidea:employee-bookings', User_Id=User_Id)

class RecruitmentView(generic.View):
    template_name = 'orchidea/Employee/Recruitment/Recruitment-Forms.html'

    def get(self, request, User_Id):
        user = get_object_or_404(User, id=User_Id)
        employee = get_object_or_404(Employee, user_ID=user)
        recruitment_forms = RecruitmentForm.objects.all()
        return render(request, self.template_name, {
            'employee': employee,
            'recruitment_forms': recruitment_forms,
            'user_type': 'employee',
            'User_Id': User_Id
        })

class SingleRecruitmentView(generic.View):
    template_name = 'orchidea/Employee/Recruitment/Single-Form.html'

    def get(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        employee = get_object_or_404(Employee, user_ID=user)
        recruitment_form = get_object_or_404(RecruitmentForm, id=pk)
        return render(request, self.template_name, {
            'employee': employee,
            'recruitment_form': recruitment_form,
            'user_type': 'employee',
            'User_Id': User_Id
        })

class AcceptRecruitmentView(generic.View):
    template_name = 'orchidea/Employee/Recruitment/AcceptForm.html'

    def get(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        employee = get_object_or_404(Employee, user_ID=user)
        recruitment_form = get_object_or_404(RecruitmentForm, id=pk)
        return render(request, self.template_name, {
            'employee': employee,
            'recruitment_form': recruitment_form,
            'user_type': 'employee',
            'User_Id': User_Id
        })

    def post(self, request, User_Id, pk):
        recruitment_form = get_object_or_404(RecruitmentForm, id=pk)
        candidate = recruitment_form.candidate_ID
        candidate_user = candidate.user_ID
        recruitment_form.status = 'Accepted'
        recruitment_form.save()
        RecruitmentForm.objects.filter(candidate_ID=candidate).exclude(id=pk).delete()
        Employee.objects.create(user_ID=candidate_user, phone_number=candidate.phone_number)
        candidate.delete()
        return redirect('orchidea:employee-recruitment', User_Id=User_Id)

class RejectRecruitmentView(generic.View):
    template_name = 'orchidea/Employee/Recruitment/RejectForm.html'

    def get(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        employee = get_object_or_404(Employee, user_ID=user)
        recruitment_form = get_object_or_404(RecruitmentForm, id=pk)
        return render(request, self.template_name, {
            'employee': employee,
            'recruitment_form': recruitment_form,
            'user_type': 'employee',
            'User_Id': User_Id
        })

    def post(self, request, User_Id, pk):
        recruitment_form = get_object_or_404(RecruitmentForm, id=pk)
        recruitment_form.delete()
        return redirect('orchidea:employee-recruitment', User_Id=User_Id)

class EmployeeProfileView(generic.View):
    template_name = 'orchidea/Employee/Profile/Profile.html'

    def get(self, request, User_Id):
        user = get_object_or_404(User, id=User_Id)
        employee = get_object_or_404(Employee, user_ID=user)
        skills = EmployeeSkill.objects.filter(employee=employee)
        return render(request, self.template_name, {
            'employee': employee,
            'skills': skills,
            'user_type': 'employee',
            'User_Id': User_Id
        })

class AddEmployeeSkillView(generic.View):
    template_name = 'orchidea/Employee/Profile/Add-Skill.html'

    def get(self, request, User_Id):
        user = get_object_or_404(User, id=User_Id)
        employee = get_object_or_404(Employee, user_ID=user)
        skills = Skill.objects.exclude(skill_employees__employee=employee)
        return render(request, self.template_name, {
            'employee': employee,
            'skills': skills,
            'user_type': 'employee',
            'User_Id': User_Id
        })

    def post(self, request, User_Id):
        user = get_object_or_404(User, id=User_Id)
        employee = get_object_or_404(Employee, user_ID=user)
        skill_id = request.POST.get('skill')
        skill = get_object_or_404(Skill, id=skill_id)
        EmployeeSkill.objects.create(employee=employee, skill=skill)
        return redirect('orchidea:profile', User_Id=User_Id)

class DeleteEmployeeSkillView(generic.View):
    template_name = 'orchidea/Employee/Profile/Delete-Skill.html'

    def get(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        employee = get_object_or_404(Employee, user_ID=user)
        employee_skill = get_object_or_404(EmployeeSkill, id=pk, employee=employee)
        return render(request, self.template_name, {
            'employee': employee,
            'employee_skill': employee_skill,
            'user_type': 'employee',
            'User_Id': User_Id
        })

    def post(self, request, User_Id, pk):
        employee_skill = get_object_or_404(EmployeeSkill, id=pk)
        employee_skill.delete()
        return redirect('orchidea:profile', User_Id=User_Id)

class CancelEmployeeBookingView(generic.View):
    template_name = 'orchidea/Employee/BookingManagement/Cancel-Booking.html'

    def get(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        employee = get_object_or_404(Employee, user_ID=user)
        booking = get_object_or_404(Booking, id=pk, employee_ID=employee)
        return render(request, self.template_name, {
            'employee': employee,
            'booking': booking,
            'User_Id': User_Id
        })

    def post(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        employee = get_object_or_404(Employee, user_ID=user)
        booking = get_object_or_404(Booking, id=pk, employee_ID=employee)
        booking.delete()
        return redirect('orchidea:employee-bookings', User_Id=User_Id)

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                        CANDIDATE-SPECIFIC VIEWS                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
class CandRegisterView(generic.View):
    template_name = 'orchidea/Register/Cand-Register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")

        if not username or not email or not password or not phone_number:
            return render(request, self.template_name, {"error": "All fields are required"})

        if User.objects.filter(email=email).exists():
            return render(request, self.template_name, {"error": "Email already registered"})

        try:
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password)
            )
            candidate = Candidate.objects.create(user_ID=user)
            request.session["candidate_id"] = candidate.id
            request.session["user_name"] = user.username
            return redirect("orchidea:homeCandidate", User_Id=user.id)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return render(request, self.template_name, {"error": "An error occurred during registration. Please try again."})

class LoginCandidateView(generic.View):
    template_name = 'orchidea/Login/Login-Cand.html'

    def get(self, request):
        logger.debug("Candidate login page accessed.")
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            logger.debug(f"Attempting login for candidate with email: {email}")
            user = User.objects.get(email=email)
            if not check_password(password, user.password):
                logger.warning(f"Password mismatch for candidate email: {email}")
                return render(request, self.template_name, {"error": "Invalid email or password"})
            candidate = Candidate.objects.get(user_ID=user)
            logger.info(f"Candidate login successful: {candidate.user_ID.username}")
            request.session["candidate_id"] = candidate.id
            request.session["user_name"] = user.username
            return redirect("orchidea:homeCandidate", User_Id=user.id)
        except User.DoesNotExist:
            logger.error(f"User not found for email: {email}")
            return render(request, self.template_name, {"error": "Invalid email or password"})
        except Candidate.DoesNotExist:
            logger.error(f"No candidate account linked to email: {email}")
            return render(request, self.template_name, {"error": "No candidate account linked to this user"})
        except Exception as e:
            logger.critical(f"Unexpected error during candidate login: {e}")
            return render(request, self.template_name, {"error": "An unexpected error occurred. Please try again."})

class HomeCandidateView(generic.View):
    template_name = 'orchidea/Candidate/Candidate-Home.html'

    def get(self, request, User_Id):
        if request.session.get("candidate_id") != User_Id:
            return HttpResponse("You are not authorized to view this page.", status=403)
        user = get_object_or_404(User, id=User_Id)
        candidate = get_object_or_404(Candidate, user_ID=user)
        return render(request, self.template_name, {
            'candidate': candidate,
            'user_type': 'candidate',
            'User_Id': User_Id
        })

class ApplyFormView(generic.View):
    template_name = 'orchidea/Candidate/Recruitment/Apply-Form.html'

    def get(self, request, User_Id):
        user = get_object_or_404(User, id=User_Id)
        candidate = get_object_or_404(Candidate, user_ID=user)
        skills = Skill.objects.all()
        return render(request, self.template_name, {
            'candidate': candidate,
            'skills': skills,
            'user_type': 'candidate',
            'User_Id': User_Id
        })

    def post(self, request, User_Id):
        user = get_object_or_404(User, id=User_Id)
        candidate = get_object_or_404(Candidate, user_ID=user)
        selected_skills = request.POST.getlist('skills[]')

        if not selected_skills or len(selected_skills) < 3:
            return render(request, self.template_name, {
                'candidate': candidate,
                'skills': Skill.objects.all(),
                'error': 'Please select at least 3 skills.',
                'user_type': 'candidate',
                'User_Id': User_Id
            })

        recruitment_form = RecruitmentForm.objects.create(candidate_ID=candidate)
        for skill_id in selected_skills:
            skill = get_object_or_404(Skill, id=skill_id)
            CandidateSkill.objects.create(form_ID=recruitment_form, skill_ID=skill)
        return redirect('orchidea:candidate-recruitment', User_Id=User_Id)

class CandidateRecruitmentView(generic.View):
    template_name = 'orchidea/Candidate/Recruitment/Recruitment-Forms.html'

    def get(self, request, User_Id):
        user = get_object_or_404(User, id=User_Id)
        candidate = get_object_or_404(Candidate, user_ID=user)
        recruitment_forms = RecruitmentForm.objects.filter(candidate_ID=candidate).prefetch_related('candidate_skills__skill_ID')
        forms_with_details = []
        for form in recruitment_forms:
            skills = [candidate_skill.skill_ID for candidate_skill in form.candidate_skills.all()]
            forms_with_details.append({
                'pk': form.pk,
                'skills': skills,
                'date': form.date,
                'status': form.status,
            })
        return render(request, self.template_name, {
            'candidate': candidate,
            'recruitment_forms': forms_with_details,
            'user_type': 'candidate',
            'User_Id': User_Id
        })

class SingleCandidateRecruitmentView(generic.View):
    template_name = 'orchidea/Candidate/Recruitment/Candidate-Single-Recruitment.html'

    def get(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        candidate = get_object_or_404(Candidate, user_ID=user)
        recruitment_form = get_object_or_404(RecruitmentForm, id=pk)
        return render(request, self.template_name, {
            'candidate': candidate,
            'recruitment_form': recruitment_form,
            'user_type': 'candidate',
            'User_Id': User_Id
        })

class WithdrawRecruitmentView(generic.View):
    template_name = 'orchidea/Candidate/Withdraw-Recruitment.html'

    def get(self, request, User_Id, pk):
        user = get_object_or_404(User, id=User_Id)
        candidate = get_object_or_404(Candidate, user_ID=user)
        recruitment_form = get_object_or_404(RecruitmentForm, id=pk)
        return render(request, self.template_name, {
            'candidate': candidate,
            'recruitment_form': recruitment_form,
            'user_type': 'candidate',
            'User_Id': User_Id
        })

    def post(self, request, User_Id, pk):
        recruitment_form = get_object_or_404(RecruitmentForm, id=pk)
        recruitment_form.delete()
        return redirect('orchidea:candidate-recruitment', User_Id=User_Id)
