from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField("date Created")

    def __str__(self):
        return self.username
    
class Skill(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    
    
class Boss(models.Model):
    Employee_Id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField("date Created")

    def __str__(self):
        return self.username
    
class Recruitee(models.Model):
    Recruit_Id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_No = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, related_name='recruitee_skills')
    created_at = models.DateTimeField("date Created")
    
    def __str__(self):
        return self.username

class Employee(models.Model):
    Employee_Id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_No = models.CharField(max_length=100)
    created_at = models.DateTimeField("date Created")
    isAdmin = models.BooleanField(default=False)
    skill_ID = models.ManyToManyField(Skill, related_name='employee_skills')
    
    # def recruit():    
    def __str__(self):
        return self.username

class Customer(models.Model):
    customer_Id = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField("date Created")
    
class Appointment(models.Model):
    user_employee_Id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    user_customer_Id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    type_of_service = models.CharField(max_length=100)
    date = models.DateTimeField("date Created")
    

    def __str__(self):
        return self.username
