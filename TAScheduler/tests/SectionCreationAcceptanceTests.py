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
        temp = Course(CourseCode="1",
                      Instructor="1",
                      CourseNumber="3")
        temp.save()
        temp = Sections(sectionCode="5",
                        parentCode="1",
                        TA=None)
        temp.save()
        self.mockClientclient.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)

    def addSection(self):
        resp = self.mockClient.post("makeSection/",{"InputSectionCode":"1","InputCourse":"1"},follow = True)
        checkSection = Course.objects.get(SectionCode="1")
        self.assertIn("1", checkSection, "Item was not added to list")
    def removeSection(self):
        pass


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
            temp = Course(CourseCode="200",
                          Instructor="1",
                          CourseNumber="3")
            temp.save()
            temp = Sections(sectionCode="5",
                            parentCode="1",
                            TA=None)
            temp.save()
        def testLoggedInAsTA(self):
            self.mockClientclient.post("/", {"InputUsername": "3", "InputPassword": "1234"}, follow=True)
            resp = self.mockClient.post("makeSection/", {"InputSectionCode": "2", "InputCourse": "1"}, follow=True)
            checkSection = Course.objects.get(SectionCode="2")
            self.assertNotIn("2", checkSection, "Item was not added to list")
        def NotFullyFilledOut(self):
            self.mockClientclient.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)
            resp = self.mockClient.post("makeSection/", {"InputSectionCode": "3", "InputCourse": ""}, follow=True)
            checkSection = Course.objects.get(SectionCode="3")
            self.assertNotIn("3", checkSection, "Item was not added to list")
            resp = self.mockClient.post("makeSection/", {"InputSectionCode": "4", "InputCourse": None}, follow=True)
            checkSection = Course.objects.get(SectionCode="4")
            self.assertNotIn("4", checkSection, "Item was not added to list")
        def AlreadyContains(self):
            self.mockClientclient.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)
            resp = self.mockClient.post("makeSection/", {"InputSectionCode": "5", "InputCourse": "200"}, follow=True)
            checkSection = Course.objects.get(SectionCode="5")
            self.assertNotIn("200", checkSection, "Item was not added to list")

            def noSectionWiththeName(self):
                pass

            def noSectionsToRemove(self):
                pass