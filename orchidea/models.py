from django.db import models
from django.utils.timezone import now
from datetime import timedelta

# Helper function to set default appointment date
def default_appointment_date():
    return now() + timedelta(days=3)

# ---------------------------
# Core User Model
# ---------------------------
class User(models.Model):
    username = models.CharField(max_length=100, unique=True, default="Cust")
    email = models.EmailField(unique=True, default="Cust@Cust.com")
    password = models.CharField(max_length=100, default="password")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# ---------------------------
# User Role Models
# ---------------------------
class Customer(models.Model):
    user_ID = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")

    def __str__(self):
        return f"Customer: {self.user_ID.username}"

class Candidate(models.Model):
    user_ID = models.OneToOneField(User, on_delete=models.CASCADE, related_name="candidate")
    phone_number = models.CharField(max_length=20, default="0000000000")

    def __str__(self):
        return f"Candidate: {self.user_ID.username}"

class Employee(models.Model):
    user_ID = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
    skills = models.ManyToManyField('Skill', through='EmployeeSkill')  # Removed the trailing comma
    phone_number = models.CharField(max_length=20, default="0000000000")

    def __str__(self):
        return f"Employee: {self.user_ID.username}"

# ---------------------------
# Skill & Join Models
# ---------------------------
class Skill(models.Model):
    name = models.CharField(max_length=150, unique=True, default="default_skill")

    def __str__(self):
        return self.name

class EmployeeSkill(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="employee_skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="skill_employees")

    class Meta:
        unique_together = ('employee', 'skill')  # Ensure no duplicate skills for the same employee

    def __str__(self):
        return f"{self.employee.user_ID.username} - {self.skill.name}"

# ---------------------------
# Recruitment Models
# ---------------------------
class RecruitmentForm(models.Model):
    candidate_ID = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="recruitment_forms")
    cand_Skills = models.ManyToManyField('Skill', through='CandidateSkill', related_name="recruitment_forms")
    status = models.CharField(max_length=50, default="pending")  # e.g., 'pending', 'accepted', etc.
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"RecruitmentForm - {self.candidate_ID.user_ID.username}"

class CandidateSkill(models.Model):
    form_ID = models.ForeignKey(RecruitmentForm, on_delete=models.CASCADE, related_name="candidate_skills")
    skill_ID = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="candidate_skills")

    def __str__(self):
        return f"{self.form_ID.candidate_ID.user_ID.username} - {self.skill_ID.name}"

class RecruitmentReview(models.Model):
    employee_ID = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="recruitment_reviews")
    form_ID = models.ForeignKey(RecruitmentForm, on_delete=models.CASCADE, related_name="recruitment_reviews")
    date = models.DateField(default=now)

    def __str__(self):
        return f"RecruitmentReview - {self.employee_ID.user_ID.username} - {self.form_ID.candidate_ID.user_ID.username}"

# ---------------------------
# Booking & Appointment
# ---------------------------
class Appointment(models.Model):
    name = models.CharField(max_length=100, default="Default Appointment")
    description = models.CharField(max_length=200, default="No description")
    duration = models.DurationField(default=timedelta(hours=1))
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Booking(models.Model):
    customer_ID = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bookings")
    employee_ID = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="bookings")
    appointment_ID = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField(default=default_appointment_date)

    def __str__(self):
        return f"Booking {self.id} - {self.customer_ID.user_ID.username} - {self.employee_ID.user_ID.username}"
