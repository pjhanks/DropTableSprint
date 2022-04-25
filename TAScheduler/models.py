from django.db import models

# Create your models here.
class MyUser(models.Model):
  userID = models.CharField(max_length=9, primary_key=True)
  name = models.CharField(max_length=20)
  address = models.CharField(max_length=40)
  email = models.CharField(max_length=20)
  phoneNumber = models.CharField(max_length=20)
  role = models.CharField(max_length=11)

class Course(models.Model):
  pass

class TA(models.Model):
  pass

class Sections(models.Model):
  sectionCode=models.CharField(max_length=10, primary_key=True)
  parentCode = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
  TA = models.ForeignKey(MyUser,on_delete=models.CASCADE, null=True)

class classTAAssignments(models.Model):
  pass
