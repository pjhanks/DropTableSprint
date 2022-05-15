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
        temp = Course(courseCode="1",
                      instructorID=instr,
                      courseNumber="3")
        temp.save()


    def test_login(self):
        resp = self.mockClient.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)
        self.assertEqual("/home/", resp.request.get("PATH_INFO"))


class testNegative(TestCase):
        def setUp(self):
            self.mockClient = Client()
            instr = MyUser(IDNumber="1",
                           name="Fred",
                           address="123 park place",
                           email="fred@uwm.edu",
                           phoneNumber="18000000000",
                           role="Instructor",
                           password="1234")
            instr.save()
        def test_loginNoUser(self):
            resp = self.mockClient.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)
            self.assertEqual("no user", resp.context.dicts[3].get("message"))
        def test_loginBadPassword(self):
            resp = self.mockClient.post("/", {"InputUsername": "1", "InputPassword": "134"}, follow=True)
            self.assertEqual("bad password", resp.context.dicts[3].get("message"))