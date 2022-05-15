import unittest
from django.test import TestCase
from TAScheduler.classes.Courses  import CoursesClass
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
        temp3 = ClassTAAssignments(AssignmentsID="1",
                                   courseCode=temp2,
                                   TAcode=temp)
        temp3.save()

    def test_Removal(self):
        PositiveTests.setUp(self)
        CoursesClass.removeTA(self, "351", "1")
        with self.assertRaises(Exception, msg="This TA Assignment does not exist"):
            ClassTAAssignments.objects.get(AssignmentsID="1")

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

    def test_TANotAssigned(self):
        NegativeTests.setUp(self)
        with self.assertRaises(RuntimeError, msg="That TA is not assigned to that course"):
            CoursesClass.removeTA(self, "351", "2")

    def test_NoTAAsignment(self):
        NegativeTests.setUp(self)
        test = ClassTAAssignments.objects.get_queryset()
        print(test)
        CoursesClass.removeTA(self, "351", "1")
        print(test)
        with self.assertRaises(Exception, msg="No TAs are assigned to this class"):
            CoursesClass.removeTA(self, "351", "1")

    def test_NoSuchClass(self):
        NegativeTests.setUp(self)
        with self.assertRaises(Exception, msg="This class does not exist"):
            CoursesClass.removeTA(self, "361", "1")


    def test_NotEnoughElements(self):
        NegativeTests.setUp(self)
        with self.assertRaises(TypeError, msg="Should not accept that few fields"):
            CoursesClass.removeTA(self, "2")


    def test_TooManyElements(self):
        NegativeTests.setUp(self)
        with self.assertRaises(TypeError, msg="Should not accept that many fields"):
            CoursesClass.removeTA(self, "2", "2", "error")
