from django.test import TestCase, Client
from TAScheduler.models import MyUser


class testPositive(TestCase):
    def setUp(self):
        self.mockClient = Client()
        temp = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Supervisor",
                      password="1234")
        temp.save()
        temp = MyUser(IDNumber="2",
                      name="Alex",
                      address="124 park place",
                      email="alex@uwm.edu",
                      phoneNumber="18000000001",
                      role="TA",
                      password="1234")
        temp.save()
        self.client.post("/", {"InputUsername": "1", "InputPassword": "1234"}, follow=True)

    def test_addTA(self):
        # add Something.addUser("user info");
        resp = self.mockClient.post("/makeUser/",
                                    {"InputIDNumber": "3", "InputName": "Ronen", "InputAddress": "122 Park place",
                                     "InputEmail": "a@uwm", "InputPhoneNumber": "18000000000", "InputRole": "TA",
                                     "InputPassword": "1234"}, follow=True)
        checkUser = MyUser.objects.get(IDNumber="3")
        self.assertIn("3", checkUser.IDNumber, "Item was not added to list")

    def test_addInstructor(self):
        resp = self.mockClient.post("/makeUser/",
                                    {"InputIDNumber": "4", "InputName": "Ronen", "InputAddress": "122 Park place",
                                     "InputEmail": "a@uwm", "InputPhoneNumber": "18000000000",
                                     "InputRole": "Instructor",
                                     "InputPassword": "1234"}, follow=True)

        checkUser = MyUser.objects.get(IDNumber="4")
        self.assertIn("4", checkUser, "Item was not added to list")

    def test_addSupervisor(self):
        resp = self.mockClient.post("/makeUser/",
                                    {"InputIDNumber": "5", "InputName": "Ronen", "InputAddress": "122 Park place",
                                     "InputEmail": "a@uwm", "InputPhoneNumber": "18000000000",
                                     "InputRole": "Supervisor",
                                     "InputPassword": "1234"}, follow=True)

        checkUser = MyUser.objects.get(IDNumber="5")
        self.assertIn("5", checkUser, "Item was not added to list")


class testNegative(TestCase):
    def setUp(self):
        self.mockClient = Client()
        temp = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Administrator",
                      password="1234")
        temp.save()
        temp = MyUser(IDNumber="2",
                      name="Alex",
                      address="124 park place",
                      email="alex@uwm.edu",
                      phoneNumber="18000000001",
                      role="TA",
                      password="1234")
        temp.save()

    def test_notSupervisor(self):
        # same ids
        self.client.post("/", {"InputUsername": "2", "InputPassword": "1234"}, follow=True)
        resp = self.mockClient.post("makeUser/",
                                    {"InputIDNumber": "3", "InputName": "Ronen", "InputAddress": "122 Park place",
                                     "InputEmail": "a@uwm", "InputPhoneNumber": "18000000000", "InputRole": "TA",
                                     "InputPassword": "1234"}, follow=True)

        checkUser = MyUser.objects.get(IDNumber="3")
        self.assertNotIn("3", checkUser, "Item was added and should not have")

    def test_notFullyFilledOut(self):
        self.client.post("/", {"InputUsername": "1", "InputPassword": "1234"}, follow=True)
        resp = self.mockClient.post("makeUser/",
                                    {"InputIDNumber": "4", "InputName": "", "InputAddress": "122 Park place",
                                     "InputEmail": "a@uwm", "InputPhoneNumber": "18000000000", "InputRole": "TA",
                                     "InputPassword": "1234"}, follow=True)
        checkUser = MyUser.objects.get(IDNumber="4")
        self.assertNotIn("4", checkUser, "Item was added and should not have")
        resp = self.mockClient.post("makeUser/",
                                    {"InputIDNumber": "3", "InputAddress": "122 Park place",
                                     "InputEmail": "a@uwm", "InputPhoneNumber": "18000000000", "InputRole": "TA",
                                     "InputPassword": "1234"}, follow=True)
        checkUser = MyUser.objects.get(IDNumber="5")
        self.assertNotIn("5", checkUser, "Item was added and should not have")
