from django.db import models

# Create your models here.

class StudentDetail(models.Model):
    name = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=20)
    branch = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    place = models.CharField(max_length=50)

class EmployeeDetails(models.Model):
    emp_name = models.CharField(max_length=50)
    emp_email = models.CharField(max_length=100)
    emp_phone = models.CharField(max_length=15)
    emp_pass = models.CharField(max_length=100)