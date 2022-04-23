from django.db import models

# Create your models here.


class MyUser(models.Model):
    userID = models.CharField(max_length=9, primary_key=True)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    phoneNumber = models.CharField(max_length=20)
    role = models.CharField(max_length=11)
    password = models.CharField(max_length=20, default="123")


class TA(models.Model):
    TACode = models.CharField(max_length=20, primary_key=True, default="42")


class Course(models.Model):
    courseCode = models.CharField(max_length=9, primary_key=True, default="12345")
    instructorID = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    TAname = models.ForeignKey(TA, on_delete=models.CASCADE, null=True)
    courseNumber = models.CharField(max_length=20, default="101")


class Sections(models.Model):
    sectionCode=models.CharField(max_length=10, primary_key=True)
    parentCode = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    TA = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)


class classTAAssignments(models.Model):
    pass