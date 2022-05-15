from django.test import TestCase, Client
from TAScheduler.models import MyUser, Course, ClassTAAssignments


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

        self.TA = MyUser.objects.create(IDNumber="3",
                                        name="ThisGuy",
                                        address="444 5th Street",
                                        email="this@that.com",
                                        phoneNumber="4568885555",
                                        role="TA",
                                        password="1234"
                                        )
        self.TA.save()

        self.TA2 = MyUser.objects.create(IDNumber="4",
                                        name="ThatPerson",
                                        address="987 6th Street",
                                        email="therb@thobe.com",
                                        phoneNumber="499832255",
                                        role="TA",
                                        password="1234"
                                         )
        self.TA2.save()

        self.courses = Course.objects.create(courseCode="1",
                                             instructorID=self.myuser,
                                             courseNumber="3")

        self.courses.save()

        self.courses = Course.objects.create(courseCode="2",
                                             instructorID=self.myuser,
                                             courseNumber="5")
        self.courses.save()

        self.mockClient.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)
        self.mockClient.post("/addTA/", {"InputCourse": "2", "InputTA": "3"}, follow=True)

    def test_addTAtoCourse(self):
        resp = self.mockClient.post("/addTA/",
                                    {"InputCourse": "1", "InputTA": "4"},
                                    follow=True)
        checkCourse = ClassTAAssignments.objects.get(courseCode="1")
        self.assertEqual("4", checkCourse.TAcode.IDNumber, "TA was not added to the course")

    def test_removeTAfromCourse(self):
        resp = self.mockClient.post("/removeTA/",
                                    {"InputCourse": "2", "InputTA": "3"},
                                    follow=True)
        with self.assertRaises(Exception, msg="That course has no TAs!"):
            ClassTAAssignments.objects.get(courseCode="2")

    def test_addSecondTAtoCourse(self):
        resp = self.mockClient.post("/addTA/",
                                    {"InputCourse": "2", "InputTA": "4"},
                                    follow=True)
        checkCourse = ClassTAAssignments.objects.get(courseCode="2")
        self.assertEqual("4", checkCourse.TAcode.IDNumber, "TA was not added to the course")

    def test_addTAtoSecondCourse(self):
        resp = self.mockClient.post("/addTA/",
                                    {"InputCourse": "1", "InputTA": "3"},
                                    follow=True)

        checkSecondCourse = ClassTAAssignments.objects.get(courseCode="1")
        self.assertEqual("3", checkSecondCourse.TAcode.IDNumber, "TA was not added to the course")

        resp = self.mockClient.post("/addTA/",
                                    {"InputCourse": "2", "InputTA": "3"},
                                    follow=True)
        checkFirstCourse = ClassTAAssignments.objects.get(courseCode="2")
        self.assertEqual("3", checkFirstCourse.TAcode.IDNumber, "TA was removed from their other course!")


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

        self.TA = MyUser.objects.create(IDNumber="3",
                                        name="ThisGuy",
                                        address="444 5th Street",
                                        email="this@that.com",
                                        phoneNumber="4568885555",
                                        role="TA",
                                        password="1234"
                                        )
        self.TA.save()

        self.TA2 = MyUser.objects.create(IDNumber="4",
                                         name="ThatPerson",
                                         address="987 6th Street",
                                         email="therb@thobe.com",
                                         phoneNumber="499832255",
                                         role="TA",
                                         password="1234"
                                         )
        self.TA2.save()

        self.courses = Course.objects.create(courseCode="1",
                                             instructorID=self.myuser,
                                             courseNumber="3")

        self.courses.save()

        self.courses = Course.objects.create(courseCode="2",
                                             instructorID=self.myuser,
                                             courseNumber="5")

        self.mockClient.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)
        self.mockClient.post("/addTA/", {"InputCourse": "2", "InputTA": "3"}, follow=True)

    def test_addSameTAtoCourse(self):
        resp = self.mockClient.post("/addTA/", {"InputCourse": "2", "InputTA": "3"}, follow=True)
        checkCourse = ClassTAAssignments.objects.get(courseCode="2")
        self.assertEqual("3", checkCourse.TAcode.IDNumber, "TA was not added to the course")


