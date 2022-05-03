import unittest
from django.test import TestCase
import TAScheduler.classes.Courses
from TAScheduler.models import MyUser, Course, ClassTAAssignments


class PositiveTests(TestCase):
    def SetUp(self):
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
        PositiveTests.SetUp(self)
        TAScheduler.classes.Courses.CoursesClass.removeTA(self,"1", "351")
        checkRemoval = ClassTAAssignments.objects.filter(AssignmentsID="1")
        self.assertEqual(0, checkRemoval.__len__(), "Entry Found")


class NegativeTests(TestCase):
    def SetUp(self):
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

    def test_noTAAssigned(self):
        NegativeTests.SetUp(self)
        with self.assertRaises(Exception, msg="This person does not exist"):
            TAScheduler.classes.Courses.CoursesClass.removeTA("2", "351")

    def test_TANotAssigned(self):
        NegativeTests.SetUp(self)
        with self.assertRaises(Exception, msg="TA not assigned to this class"):
            TAScheduler.classes.Courses.CoursesClass.removeTA("3", "351")

    def test_NoSuchClass(self):
        NegativeTests.SetUp(self)
        with self.assertRaises(Exception, msg="This class does not exist"):
            TAScheduler.classes.Courses.CoursesClass.removeTA("1", "361")


    def test_NotEnoughElements(self):
        NegativeTests.SetUp(self)
        with self.assertRaises(TypeError, msg="Should not accept that few fields"):
            TAScheduler.classes.Courses.CoursesClass.removeTA("2")


    def test_TooManyElements(self):
        NegativeTests.SetUp(self)
        with self.assertRaises(TypeError, msg="Should not accept that many fields"):
            TAScheduler.classes.Courses.CoursesClass.removeTA(self, "2", "2", "error")