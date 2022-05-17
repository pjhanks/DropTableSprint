from django.test import TestCase, Client
from TAScheduler.models import MyUser, Course


class testPositive(TestCase):
    def setUp(self):
        self.mockClient = Client()
        self.instr1 = MyUser.objects.create(IDNumber="1",
                       name="Fred",
                       address="123 park place",
                       email="fred@uwm.edu",
                       phoneNumber="18000000000",
                       role="Instructor",
                       password="1234")
        self.instr1.save()
        self.instr2 = MyUser.objects.create(IDNumber="2",
                       name="John",
                       address="123 park place",
                       email="john@uwm.edu",
                       phoneNumber="18000000000",
                       role="Instructor",
                       password="1234")
        self.instr2.save()
        self.courses1 = Course.objects.create(courseCode="351",
                       instructorID=None,
                       courseNumber="101")
        self.courses1.save()
        self.courses2 = Course.objects.create(courseCode="479",
                       instructorID=self.instr2,
                       courseNumber="101")
        self.course2.save()
        self.instr3 = Course.objects.create(courseCode="337",
                       instructorID=self.instr1,
                       courseNumber="101")
        self.instr3.save()
        self.mockClient.post("/", {"InputCourseCode": "1"}, follow=True)

    def test_removeInstructor(self):
        resp = self.mockClient.post("/removeInstructor/", {"InputCourseCode": "1"}, follow=True)
        checkCourse = Course.objects.get(courseCode="1")
        self.assertEqual("1", checkCourse, "Instructor was not removed")


class testNegative(TestCase):
    def setUp(self):
        self.mockClient = Client()
        self.instr1 = MyUser.objects.create(IDNumber="1",
                                            name="Fred",
                                            address="123 park place",
                                            email="fred@uwm.edu",
                                            phoneNumber="18000000000",
                                            role="Instructor",
                                            password="1234")
        self.instr1.save()
        self.instr2 = MyUser.objects.create(IDNumber="2",
                                            name="John",
                                            address="123 park place",
                                            email="john@uwm.edu",
                                            phoneNumber="18000000000",
                                            role="Instructor",
                                            password="1234")
        self.instr2.save()
        self.courses1 = Course.objects.create(courseCode="351",
                                              instructorID=None,
                                              courseNumber="101")
        self.courses1.save()
        self.course2 = Course.objects.create(courseCode="479",
                                              instructorID=self.instr2,
                                              courseNumber="101")
        self.course2.save()
        self.instr3 = Course.objects.create(courseCode="337",
                                            instructorID=self.instr1,
                                            courseNumber="101")
        self.instr3.save()
        self.mockClient.post("/", {"InputCourseCode": "1"}, follow=True)

    def test_unassignNotFullyFilledOut(self):
        self.mockClient.post("/", {"InputCourseCode": "2"}, follow=True)
        resp = self.mockClient.post("/removeInstructor/", {"InputSectionCode": ""}, follow=True)
        checkCourse = Course.objects.get(courseCode="")
        self.assertNotIn("", checkCourse, "Item was not added to list")
        resp = self.mockClient.post("/removeInstructor/", {"InputCourseCode": None}, follow=True)
        checkCourse = Course.objects.get(sectionCode=None)
        self.assertNotIn(None, checkCourse, "Item was not added to list")

    def test_NoInstructorToRemove(self):
        self.mockClient.post("/", {"InputCourseCode": "3"}, follow=True)
        resp = self.mockClient.post("/removeInstructor/", {"InputCourseCode": "3"}, follow=True)
        checkCourse = Course.objects.get(courseCode="3")
        self.assertNotIn("3", checkCourse, "Item was not added to list")

    def test_noCourseEntered(self):
        self.mockClient.post("/", {"InputCourseCode": "2"}, follow=True)
        resp = self.mockClient.post("/removeInstructor/", follow=True)
        checkCourse = Course.objects.get(courseCode="")
        self.assertNotIn("", checkCourse, "Item was missing Course")
