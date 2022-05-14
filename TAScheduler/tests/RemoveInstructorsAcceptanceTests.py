from django.test import TestCase, Client
from TAScheduler.models import MyUser, Course


class testPositive(TestCase):
    def setUp(self):
        self.mockClient = Client()
        temp1 = MyUser(IDNumber="1",
                       name="Fred",
                       address="123 park place",
                       email="fred@uwm.edu",
                       phoneNumber="18000000000",
                       role="Instructor",
                       password="1234")
        temp1.save()
        temp2 = MyUser(IDNumber="2",
                       name="John",
                       address="123 park place",
                       email="john@uwm.edu",
                       phoneNumber="18000000000",
                       role="Instructor",
                       password="1234")
        temp2.save()
        temp3 = Course(courseCode="351",
                       instructorID=None,
                       courseNumber="101")
        temp3.save()
        temp4 = Course(courseCode="479",
                       instructorID=temp2,
                       courseNumber="101")
        temp4.save()
        temp5 = Course(courseCode="337",
                       instructorID=temp1,
                       courseNumber="101")
        temp5.save()
        self.mockClient.post("/", {"InputCourseCode": "1"}, follow=True)

    def test_removeInstructor(self):
        resp = self.mockClient.post("/removeInstructor/", {"InputCourseCode": "1"}, follow=True)
        checkCourse = Course.objects.get(courseCode="1")
        self.assertEqual("1", checkCourse, "Instructor was not removed")


class testNegative(TestCase):
    def setUp(self):
        self.mockClient = Client()
        temp1 = MyUser(IDNumber="1",
                       name="Fred",
                       address="123 park place",
                       email="fred@uwm.edu",
                       phoneNumber="18000000000",
                       role="Instructor",
                       password="1234")
        temp1.save()
        temp2 = MyUser(IDNumber="2",
                       name="Fred",
                       address="123 park place",
                       email="fred@uwm.edu",
                       phoneNumber="18000000000",
                       role="Supervisor",
                       password="1234")
        temp2.save()

        temp3 = Course(courseCode="351",
                       instructorID=None,
                       courseNumber="3")
        temp3.save()
        temp4 = Course(courseCode="479",
                       instructorID=temp2,
                       courseNumber="101")
        temp4.save()
        temp5 = Course(courseCode="337",
                       instructorID=temp1,
                       courseNumber="101")
        temp5.save()
        self.mockClient.post("/", {"InputCourseCode": "1"}, follow=True)

    def test_unassignNotFullyFilledOut(self):
        self.mockClientclient.post("/", {"InputCourseCode": "2"}, follow=True)
        resp = self.mockClient.post("/removeInstructor/", {"InputSectionCode": ""}, follow=True)
        checkCourse = Course.objects.get(courseCode="")
        self.assertNotIn("", checkCourse, "Item was not added to list")
        resp = self.mockClient.post("/removeInstructor/", {"InputCourseCode": None}, follow=True)
        checkCourse = Course.objects.get(sectionCode=None)
        self.assertNotIn(None, checkCourse, "Item was not added to list")

    def test_NoInstructorToRemove(self):
        self.mockClientclient.post("/", {"InputCourseCode": "3"}, follow=True)
        resp = self.mockClient.post("/removeInstructor/", {"InputCourseCode": "3"}, follow=True)
        checkCourse = Course.objects.get(courseCode="3")
        self.assertNotIn("3", checkCourse, "Item was not added to list")

    def test_noCourseEntered(self):
        self.mockClientclient.post("/", {"InputCourseCode": "2"}, follow=True)
        resp = self.mockClient.post("/removeInstructor/", follow=True)
        checkCourse = Course.objects.get(courseCode="")
        self.assertNotIn("", checkCourse, "Item was missing Course")
