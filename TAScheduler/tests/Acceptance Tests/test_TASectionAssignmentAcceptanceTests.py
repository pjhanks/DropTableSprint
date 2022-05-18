from django.test import TestCase, Client
from TAScheduler.models import MyUser, Course, Sections, ClassTAAssignments

class tests(TestCase):
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
        self.TA3 = MyUser.objects.create(IDNumber="5",
                                         name="ThatPerson",
                                         address="987 6th Street",
                                         email="therb@thobe.com",
                                         phoneNumber="499832255",
                                         role="TA",
                                         password="1234"
                                         )
        self.TA3.save()

        self.courses = Course.objects.create(courseCode="1",
                                             instructorID=self.myuser,
                                             courseNumber="3")

        self.courses.save()

        self.courses = Course.objects.create(courseCode="2",
                                             instructorID=self.myuser,
                                             courseNumber="5")
        self.courses.save()
        self.mySection = Sections.objects.create(sectionCode="3",
                                                 parentCode =self.courses ,
                                                 TA = None)
        self.mySection.save()
        self.mySection = Sections.objects.create(sectionCode="4",
                                                 parentCode=self.courses,
                                                 TA=self.TA2)
        self.mySection.save()
        self.ca1= ClassTAAssignments.objects.create(AssignmentsID="1",
                                                    courseCode=self.courses,
                                                    TAcode=self.TA)
        self.ca1.save()
        self.ca1 = ClassTAAssignments.objects.create(AssignmentsID="1",
                                                     courseCode=self.courses,
                                                     TAcode=self.TA2)
        self.ca1.save()

        self.mockClient.post("/", {"InputUsername": "1  ", "InputPassword": "1234"}, follow=True)
    def test_AssignTA(self):
        resp = self.mockClient.post("/sectionTemplates/addTAsec.html",{"sectionCode":"3", "TAcode": "3"},follow=True)
        checkSection = Sections.objects.filter(sectionCode="3")[0]
        self.assertEqual(checkSection.TA,"3", "Assign TA failed")
    def test_AssignTAFull(self):
        resp = self.mockClient.post("/sectionTemplates/addTAsec.html", {"sectionCode": "4", "TAcode": "3"}, follow=True)
        checkSection = Sections.objects.filter(sectionCode="4")[0]
        self.assertEqual(checkSection.TA, "4", "TA chenged")
    def test_NotAssignedToParent(self):
        resp = self.mockClient.post("/sectionTemplates/addTAsec.html", {"sectionCode": "3", "TAcode": "5"}, follow=True)
        checkSection = Sections.objects.filter(sectionCode="3")[0]
        self.assertEqual(checkSection.TA, None, "TA not in course assigned")
    def test_NotTA(self):
        resp = self.mockClient.post("/sectionTemplates/addTAsec.html", {"sectionCode": "3", "TAcode": "2"}, follow=True)
        checkSection = Sections.objects.filter(sectionCode="3")[0]
        self.assertEqual(checkSection.TA, None, "Not TA assigned")
    def test_notLoggedInAsInstructor(self):
        self.mockClient.post("/", {"InputUsername": "3  ", "InputPassword": "1234"}, follow=True)
        resp = self.mockClient.post("/sectionTemplates/addTAsec.html", {"sectionCode": "3", "TAcode": "3"}, follow=True)
        checkSection = Sections.objects.filter(sectionCode="3")[0]
        self.assertEqual(checkSection.TA, "3", "Assigned TA while logged in as a TA")

