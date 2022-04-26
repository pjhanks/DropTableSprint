from django.test import TestCase, Client
from TAScheduler.models import MyUser,Course,Sections

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
        temp = Course(courseCode="1",
                      Instructor="1",
                      courseNumber="3")
        temp.save()
        temp = Sections(sectionCode="5",
                        parentCode="1",
                        TA=None)
        temp.save()
        self.mockClientclient.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)

    def addSection(self):
        resp = self.mockClient.post("makeSection/",{"InputSectionCode":"1","InputCourse":"1"},follow = True)
        checkSection = Sections.objects.get(sectionCode="1")
        self.assertIn("1", checkSection, "Item was not added to list")
    def removeSection(self):
        resp = self.mockClient.post("removeCourse/", {"InputSectionCode": "5"})
        checkSection = Sections.objects.get(sectionCode="1")
        self.assertNotIn("1", checkSection, "Course was not removed")


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
            temp = Course(courseCode="1",
                          instructorID="1",
                          courseNumber="3")
            temp.save()
            temp = Course(courseCode="200",
                          instructorID="1",
                          courseNumber="3")
            temp.save()
            temp = Sections(sectionCode="5",
                            parentCode="1",
                            TA=None)
            temp.save()
        def testLoggedInAsTA(self):
            self.mockClientclient.post("/", {"InputUsername": "3", "InputPassword": "1234"}, follow=True)
            resp = self.mockClient.post("makeSection/", {"InputSectionCode": "2", "InputCourse": "1"}, follow=True)
            checkSection = Sections.objects.get(sectionCode="2")
            self.assertNotIn("2", checkSection, "Item was not added to list")
        def NotFullyFilledOut(self):
            self.mockClientclient.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)
            resp = self.mockClient.post("makeSection/", {"InputSectionCode": "3", "InputCourse": ""}, follow=True)
            checkSection = Sections.objects.get(sectionCode="3")
            self.assertNotIn("3", checkSection, "Item was not added to list")
            resp = self.mockClient.post("makeSection/", {"InputSectionCode": "4", "InputCourse": None}, follow=True)
            checkSection = Sections.objects.get(sectionCode="4")
            self.assertNotIn("4", checkSection, "Item was not added to list")
        def AlreadyContains(self):
            self.mockClientclient.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)
            resp = self.mockClient.post("makeSection/", {"InputSectionCode": "5", "InputCourse": "200"}, follow=True)
            checkSection = Sections.objects.get(sectionCode="5")
            self.assertNotIn("200", checkSection, "Item was not added to list")

            def noSectionWiththeName(self):
                resp = self.mockClient.post("removeSection/", {"InputSectionCode": "300"})
                checkSection = Sections.objects.get(courseCode="300")
                self.assertNotIn("300", checkSection, "Course was added somehow")