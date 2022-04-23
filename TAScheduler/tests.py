from django.test import TestCase, Client
from TAScheduler.models import MyUser, Sections, Course, TA


class LoginTests(TestCase):
    client = None
    sectionList = None
    courses = None

    def setUp(self):
        self.client = Client()
        self.courses = Course()
        self.sectionList = {"one": ["101", self.courses.courseCode], "two": ["201", self.courses.courseCode]}

        # fill test database
        for i in self.sectionList.keys():
            temp = MyUser(name=i, password=i)
            temp.save()
            # Sections(sectionCode=self.sectionList[i][0], parentCode=self.sectionList[i][1], TA=temp).save()
            Sections(sectionCode=self.sectionList[i][0], parentCode=self.courses.courseCode, TA=temp).save()

    def test_Good_Password(self):
        for i in self.sectionList.keys():
            resp = self.client.post("/", {"name": i, "password": i}, follow=True)
            self.assertEqual(resp.context['message'], 'bad password')

    def test_Bad_Password(self):
        for i in self.sectionList.keys():
            resp = self.client.post("/", {"name": i, "password": 'i'}, follow=True)
            self.assertEqual(resp.context['message'], 'bad password')

    def test_No_Password(self):
        for i in self.sectionList.keys():
            resp = self.client.post("/", {"name": i, "password": ''}, follow=True)
            self.assertEqual(resp.context['message'], 'bad password')

    def test_Incorrect_Name(self):
        for i in self.sectionList.keys():
            resp = self.client.post("/", {"name": 'NotARealUserName', "password": i}, follow=True)
            self.assertEqual(resp.context['message'], 'Username does not exist')

    def test_No_Name(self):
        for i in self.sectionList.keys():
            resp = self.client.post("/", {"name": '', "password": i}, follow=True)
            self.assertEqual(resp.context['message'], 'Username cannot be blank')




