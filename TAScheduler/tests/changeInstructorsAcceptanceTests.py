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
        self.courses2.save()
        self.courses3 = Course.objects.create(courseCode="337",
                                            instructorID=self.instr1,
                                            courseNumber="101")
        self.courses3.save()
        self.mockClient.post("/", {"InputCourseCode": "1", "InputIDNumber": "2"}, follow=True)

    def test_changeInstructor(self):
        resp = self.mockClient.post("/addInstructor/", {"InputCourseCode": "1", "InputIDNumber": "1"}, follow=True)
        checkCourse = Course.objects.get(courseCode="1")
        self.assertEqual("1", checkCourse, "Item was not added to list")

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
        self.courses2 = Course.objects.create(courseCode="479",
                                              instructorID=self.instr2,
                                              courseNumber="101")
        self.courses2.save()
        self.courses3 = Course.objects.create(courseCode="337",
                                            instructorID=self.instr1,
                                            courseNumber="101")
        self.courses3.save()
        self.mockClient.post("/", {"InputCourseCode": "1", "InputIDNumber": "2"}, follow=True)

    def test_assignNotFullyFilledOut(self):
        self.mockClient.post("/", {"InputCourseCode": "1", "InputIDNumber": "2"}, follow=True)
        resp = self.mockClient.post("/addInstructor/", {"InputCourseCode": "2", "InputIDNumber": ""}, follow=True)
        checkCourse = Course.objects.get(courseCode="2")
        self.assertNotIn("2", checkCourse, "Item was not added to list")
        resp = self.mockClient.post("/addInstructor/", {"InputCourseCode": "2", "InputIDNumber": None}, follow=True)
        checkCourse = Course.objects.get(courseCode="2")
        self.assertNotIn("2", checkCourse, "Item was not added to list")

    def test_alreadyContainsSpecifiedInstructor(self):
        self.mockClient.post("/", {"InputCourseCode": "2", "InputIDNumber": "1"}, follow=True)
        resp = self.mockClient.post("/addInstructor/", {"InputCourseCode": "1", "InputIDNumber": "1"}, follow=True)
        checkCourse = Course.objects.get(courseCode="1")
        self.assertNotIn("1", checkCourse, "Item was not added to list")

    def test_noInstructorAttached(self):
        self.mockClient.post("/", {"InputCourseCode": "2", "InputIDNumber": "1"}, follow=True)
        resp = self.mockClient.post("/addInstructor/", {"InputCourseCode": "1"})
        checkCourse = Course.objects.get(courseCode="1")
        self.assertNotIn("300", checkCourse, "Item was missing Instructor ID")

    def test_noCourseEntered(self):
        self.mockClient.post("/", {"InputCourseCode": "2", "InputIDNumber": "1"}, follow=True)
        resp = self.mockClient.post("/addInstructor/", {"InputCourseCode": ""}, follow=True)
        checkCourse = Course.objects.get(courseCode="")
        self.assertNotIn("", checkCourse, "Item missing Course")
