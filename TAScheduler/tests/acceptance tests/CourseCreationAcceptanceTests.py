from django.test import TestCase, Client
from TAScheduler.models import MyUser, Course


class testPositive(TestCase):
    def setUp(self):
        self.mockClient = Client()

        self.myuser = MyUser.objects.create(IDNumber="1",
                                            name="Fred",
                                            address="123 park place",
                                            email="fred@uwm.edu",
                                            phoneNumber="18000000000",
                                            role="Instructor",
                                            password="1234")
        self.myuser.save()

        self.admin = MyUser.objects.create(IDNumber="2",
                                           name="Fred",
                                           address="123 park place",
                                           email="fred@uwm.edu",
                                           phoneNumber="18000000000",
                                           role="Supervisor",
                                           password="1234")
        self.admin.save()

        self.courses = Course.objects.create(courseCode="1",
                                             instructorID=self.myuser,
                                             courseNumber="3")

        self.courses.save()

        self.mockClient.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)

    def test_addCourseWithoutInstructor(self):
        resp = self.mockClient.post("/makeCourse/",
                                    {"InputCourseCode": "3", "InputCourseNumber": "101", "InputInstructor": ""},
                                    follow=True)
        checkCourse = Course.objects.get(courseCode="3")
        self.assertEqual("3", checkCourse.courseCode, "Item was not added to list")

    def test_addCourseWithInstructor(self):
        resp = self.mockClient.post("/makeCourse/",
                                    {"InputCourseCode": "4", "InputCourseNumber": "101", "InputInstructor": "1"},
                                    follow=True)

        checkCourse = Course.objects.get(courseCode="4")
        self.assertEqual("4", checkCourse.courseCode, "Item was not added to list")

    def test_removeCourse(self):
        resp = self.mockClient.post("/removeCourse/", {"InputCourse": "1"})
        checkCourse = Course.objects.filter(courseCode="1")
        self.assertEqual(0, checkCourse.count(), "Course was not removed")


class testNegative(TestCase):
    def setUp(self):
        self.mockClient = Client()

        self.myuser = MyUser.objects.create(IDNumber="1",
                                            name="Fred",
                                            address="123 park place",
                                            email="fred@uwm.edu",
                                            phoneNumber="18000000000",
                                            role="Instructor",
                                            password="1234")
        self.myuser.save()

        self.admin = MyUser.objects.create(IDNumber="2",
                                           name="Fred",
                                           address="123 park place",
                                           email="fred@uwm.edu",
                                           phoneNumber="18000000000",
                                           role="Supervisor",
                                           password="1234")
        self.admin.save()

        self.courses = Course.objects.create(courseCode="1",
                                             instructorID=self.myuser,
                                             courseNumber="3")

        self.courses.save()

    def test_testLoggedInAsTA(self):
        self.mockClient.post("/", {"InputUsername": "3", "InputPassword": "1234"}, follow=True)
        x = self.mockClient.session["username"] = "3"
        resp = self.mockClient.get("/makeCourse/", {"username": x})

        checkCourse = Course.objects.get(courseCode="5")

        self.assertEqual("5", checkCourse.courseCode, "Item was not supposed added to list")

    def test_NotFullyFilledOut(self):
        self.mockClient.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)
        resp = self.mockClient.post("/makeCourse/",
                                    {"InputCourseCode": "6", "InputCourseNumber": "", "InputInstructor": ""},
                                    follow=True)
        checkCourse = Course.objects.get(courseCode="6")
        self.assertNotEqual("6", checkCourse.courseCode, "Item was not supposed added to list")
        resp = self.mockClient.post("/makeCourse/",
                                    {"InputCourseCode": "7", "InputCourseNumber": "", "InputInstructor": ""},
                                    follow=True)
        checkCourse = Course.objects.get(courseCode="7")
        self.assertNotEqual("7", checkCourse.courseCode, "Item was not supposed added to list")


