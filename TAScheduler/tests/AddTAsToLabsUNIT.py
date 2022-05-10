from django.test import TestCase
from TAScheduler.classes import Sections as Section
from TAScheduler.models import MyUser, Course, Sections


class positiveTests(TestCase):
    def setUp(self):
        TA1 = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="TA",
                      password="1234")
        TA1.save()
        TA2 = MyUser(IDNumber="2",
                      name="John",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="TA",
                      password="1234")
        TA2.save()
        temp = Course(courseCode="1",
                      instructorID=None,
                      courseNumber="3")
        temp.save()
        temp2 = Sections(sectionCode="1",
                      parentCode=temp,
                      TA=None)
        temp2.save()
        temp2 = Sections(sectionCode="2",
                         parentCode=temp,
                         TA=TA1)
        temp2.save()

    def test_NonetoSome(self):
        positiveTests.setUp(self)
        Section.SectionsClass.assignTA(self, "1", "1")
        checkSection = Sections.objects.filter(sectionCode="1")
        self.assertEqual(checkSection[0].TA, "1")

    def testSomeToSome(self):
        positiveTests.setUp(self)
        Section.SectionsClass.assignTA(self, "2", "2")
        checkSection = Sections.objects.filter(sectionCode="1")
        self.assertEqual(checkSection[0].TA, "2")


class negativeTests(TestCase):
    def setUp(self):
        TA1 = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="TA",
                      password="1234")
        TA1.save()
        NotTA = MyUser(IDNumber="2",
                      name="John",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Instructor",
                      password="1234")
        NotTA.save()
        temp = Course(courseCode="1",
                      instructorID=None,
                      courseNumber="3")
        temp.save()
        temp2 = Sections(sectionCode="1",
                         parentCode=temp,
                         TA=None)
        temp2.save()
        temp2 = Sections(sectionCode="2",
                         parentCode=temp,
                         TA=TA1)
        temp2.save()

    def testNotInstructor(self):
        Section.SectionsClass.assignTA(self, "2", "2")
        checkSection = Section.objects.filter(sectionCode="1")
        self.assertNotEqual(checkSection[0].TA, "2")

    def testNotEnoughElements(self):
        with self.assertRaises(TypeError, msg="Should not accept that few fields"):
            Section.sectionClass.assignTA("2")

    def testTooManyElements(self):
        with self.assertRaises(TypeError, msg="Should not accept that many fields"):
            Section.sectionClass.assignTA(self, "2", "2", "error")
