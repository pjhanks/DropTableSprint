import unittest
from django.test import TestCase
from TAScheduler.classes.Courses import CoursesClass
from TAScheduler.models import MyUser, Course, ClassTAAssignments


class PositiveTests(TestCase):
    def setUp(self):
        temp = MyUser(IDNumber="1",
                      name="Alex",
                      address="124 park place",
                      email="alex@uwm.edu",
                      phoneNumber="18000000001",
                      role="TA",
                      password="123")
        temp.save()
        temp2 = Course(courseCode="351",
                       instructorID=None,
                       courseNumber="101")
        temp2.save()


    def test_Assign(self):

        CoursesClass.assignTA(self, "351", "1")
        TAobj = ClassTAAssignments.objects.get(TAcode="1")
        self.assertEqual("351", TAobj.courseCode.courseCode, "TA was not assigned properly")


class NegativeTests(TestCase):
    def setUp(self):
        temp = MyUser(IDNumber="1",
                      name="Alex",
                      address="124 park place",
                      email="alex@uwm.edu",
                      phoneNumber="18000000001",
                      role="TA",
                      password="123")
        temp.save()
        notAssigned = MyUser(IDNumber="3",
                      name="Alex",
                      address="124 park place",
                      email="alex@uwm.edu",
                      phoneNumber="18000000001",
                      role="TA",
                      password="123")
        notAssigned.save()
        temp2 = Course(courseCode="351",
                       instructorID=None,
                       courseNumber="101")
        temp2.save()
        temp3 = ClassTAAssignments(AssignmentsID="1",
                                   courseCode=temp2,
                                   TAcode=temp)
        temp3.save()

    def test_TAAssigned(self):

        course = Course.objects.get(courseCode="351")
        TA = MyUser.objects.get(IDNumber="1")
        with self.assertRaises(RuntimeError, msg="That TA is already assigned to this course!"):
            CoursesClass.assignTA(self, "351", "1")

    #check for no such course
    #no such TA

    def test_TANotAssigned(self):

        with self.assertRaises(Exception, msg="TA not assigned to this class"):
            CoursesClass.removeTA(self, "351", "3")

    def test_NoSuchClass(self):

        with self.assertRaises(Exception, msg="This class does not exist"):
            CoursesClass.removeTA(self, "361", "1")


    def test_NotEnoughElements(self):

        with self.assertRaises(TypeError, msg="Should not accept that few fields"):
            CoursesClass.removeTA(self, "2")


    def test_TooManyElements(self):

        with self.assertRaises(TypeError, msg="Should not accept that many fields"):
            CoursesClass.removeTA(self, "2", "2", "error")
