from django.db import models

# Create your models here.


class MyUser(models.Model):
    IDNumber = models.CharField(max_length=9, primary_key=True)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=40)
    email = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=20)
    role = models.CharField(max_length=11)
    password = models.CharField(max_length=20)


class TA(models.Model):
    TACode = models.CharField(max_length=20, primary_key=True, default="42")
    TAID = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.TACode

class Course(models.Model):
    courseCode = models.CharField(max_length=9, primary_key=True, default="12345")
    instructorID = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    TAs = models.ForeignKey(TA, on_delete=models.CASCADE, null=True)
    courseNumber = models.CharField(max_length=20, default="101")

    def __str__(self):
        return self.courseCode

class Sections(models.Model):
    sectionCode = models.CharField(max_length=10, primary_key=True)
    parentCode = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    TA = models.ForeignKey(TA, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.sectionCode

class ClassTAAssignments(models.Model):
    AssignmentsID = models.CharField(max_length=50, primary_key=True)
    courseCode = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    TAcode = models.ForeignKey(TA, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.AssignmentsID
