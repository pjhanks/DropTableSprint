from django.test import TestCase, Client
from TAScheduler.models import MyUser,Course

class testPositive(TestCase):
    def setUp(self):
        self.mockClient=Client()
        instr = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Instructor",
                      password="1234")
        instr.save()
        admin = MyUser(IDNumber="2",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Supervisor",
                      password="1234")
        admin.save()
        temp = Course(CourseCode="1",
                      Instructor="1",
                      CourseNumber="3")
        temp.save()
        self.mockClientclient.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)

    def addCourseWithoutInstructor(self):
        resp = self.mockClient.post("makeCourse/",{"InputCourseCode":"3","InputCourseNumber":"101","InputInstructor":None},follow = True)
        checkCourse = Course.objects.get(CourseCode="3")
        self.assertIn("3", checkCourse, "Item was not added to list")
    def addCourseWithInstructor(self):
        resp = self.mockClient.post("makeCourse/",
                                    {"InputCourseCode": "4", "InputCourseNumber": "101", "InputInstructor": "1"},
                                    follow=True)
        checkCourse = Course.objects.get(CourseCode="4")
        self.assertIn("4", checkCourse, "Item was not added to list")

class testNegative(TestCase):
        def setup(self):
            self.mockClient = Client()
            instr = MyUser(IDNumber="1",
                           name="Fred",
                           address="123 park place",
                           email="fred@uwm.edu",
                           phoneNumber="18000000000",
                           role="Instructor",
                           password="1234")
            instr.save()
            admin = MyUser(IDNumber="2",
                           name="Fred",
                           address="123 park place",
                           email="fred@uwm.edu",
                           phoneNumber="18000000000",
                           role="Supervisor",
                           password="1234")
            admin.save()
            TA = MyUser(IDNumber="3",
                           name="Fred",
                           address="123 park place",
                           email="fred@uwm.edu",
                           phoneNumber="18000000000",
                           role="TA",
                           password="1234")
            temp = Course(CourseCode="1",
                          Instructor="1",
                          CourseNumber="3")
            temp.save()
        def testLoggedInAsTA(self):
            self.mockClientclient.post("/", {"InputUsername": "3", "InputPassword": "1234"}, follow=True)
            resp = self.mockClient.post("makeCourse/",
                                        {"InputCourseCode": "5", "InputCourseNumber": "101", "InputInstructor": None},
                                        follow=True)
            checkCourse = Course.objects.get(CourseCode="5")
            self.assertNotIn("5", checkCourse, "Item was not supposed added to list")
        def NotFullyFilledOut(self):
            self.mockClientclient.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)
            resp = self.mockClient.post("makeCourse/",
                                        {"InputCourseCode": "6", "InputCourseNumber": "", "InputInstructor": None},
                                        follow=True)
            checkCourse = Course.objects.get(CourseCode="6")
            self.assertNotIn("7", checkCourse, "Item was not supposed added to list")
            resp = self.mockClient.post("makeCourse/",
                                        {"InputCourseCode": "7", "InputCourseNumber": None, "InputInstructor": None},
                                        follow=True)
            checkCourse = Course.objects.get(CourseCode="7")
            self.assertNotIn("6", checkCourse, "Item was not supposed added to list")