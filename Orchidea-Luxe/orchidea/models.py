from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField("date Created")

    def __str__(self):
        return self.username
    
    def create_user(self, username, email, password):
        user = self.create(username=username, email=email, password=password)
        return user
    
class Admin(models.Model):
    user_Id = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField("date Created")

    def __str__(self):
        return self.username
    
class Recruit(models.Model):
    user_Id = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField("date Created")

class Customer(models.Model):

class Appointment(models.Model):
    customer_id
    employee_id


    def __str__(self):
        return self.username

