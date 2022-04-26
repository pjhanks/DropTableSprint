from django.test import TestCase, Client
from TAScheduler.models import MyUser

class testPositive(TestCase):
    def setUp(self):
        self.mockClient=Client()
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
        self.mockClient.post("/",{"InputUsername":"1","InputPassword":"1234"},follow=True)

    def test_addTA(self):
        # add Something.addUser("user info");
        resp = self.mockClient.post("/makeUser/",{"InputIDNumber":"3","InputName":"Ronen","InputAddress":"122 Park place","InputEmail":"a@uwm","InputPhoneNumber":"18000000000","InputRole":"TA","InputPassword":"1234"},follow=True)
        checkUser = list(MyUser.objects.filter(IDNumber="3"))
        if(checkUser.__len__()>0):
            self.assertIn("3", checkUser[0].IDNumber, "Item was not added to list")
    def test_addInstructor(self):
        resp = self.mockClient.post("/makeUser/",
                                    {"InputIDNumber": "4", "InputName": "Ronen", "InputAddress": "122 Park place",
                                     "InputEmail": "a@uwm", "InputPhoneNumber": "18000000000", "InputRole": "Instructor",
                                     "InputPassword": "1234"}, follow=True)

        checkUser = list(MyUser.objects.filter(IDNumber="4"))
        if(checkUser.__len__()>0):
            self.assertEqual("4", checkUser[0].IDNumber, "Item was not added to list")
    def test_addSupervisor(self):
        resp = self.mockClient.post("/makeUser/",
                                    {"InputIDNumber": "5", "InputName": "Ronen", "InputAddress": "122 Park place",
                                     "InputEmail": "a@uwm", "InputPhoneNumber": "18000000000", "InputRole": "Supervisor",
                                     "InputPassword": "1234"}, follow=True)

        checkUser = list(MyUser.objects.filter(IDNumber="5"))
        if(checkUser.__len__()>0):
            self.assertEqual("5", checkUser[0].IDNumber, "Item was not added to list")
    def test_removeUser(self):
        pass



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

    def test_notFullyFilledOut(self):
        self.mockClient.post("/",{"InputUsername":"1","InputPassword":"1234"},follow=True)
        resp = self.mockClient.post("/makeUser/",
                                    {"InputIDNumber": "4", "InputName": "", "InputAddress": "122 Park place",
                                     "InputEmail": "a@uwm", "InputPhoneNumber": "18000000000", "InputRole": "TA",
                                     "InputPassword": "1234"}, follow=True)
        checkUser = list(MyUser.objects.filter(IDNumber="4"))
        self.assertNotEqual("4", checkUser, "Item was added and should not have")
        resp = self.mockClient.post("/makeUser/",
                                    {"InputIDNumber": "3", "InputName":"","InputAddress": "122 Park place",
                                     "InputEmail": "a@uwm", "InputPhoneNumber": "18000000000", "InputRole": "TA",
                                     "InputPassword": "1234"}, follow=True)

        checkUser = list(MyUser.objects.filter(IDNumber="5"))
        if(checkUser.__len__()>0):
            self.assertNotEqual("5", checkUser[0].IDNumber, "Item was added and should not have")
class removeUserTests(TestCase):
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
        self.mockClient.post("/", {"InputUsername": "1", "InputPassword": "1234"}, follow=True)
    def test_removeUser(self):
        checkUser = list(MyUser.objects.filter(IDNumber="2"))
        resp = self.mockClient.post("/removeUser/",{"InputUser": "2"})
        checkUser = list(MyUser.objects.filter(IDNumber="2"))
        if (checkUser.__len__() > 0):
            self.assertNotEqual("2", checkUser[0].IDNumber, "User was not removed")
    def test_attemptToRemoveYourself(self):
        def removeUser(self):
            checkUser = list(MyUser.objects.filter(IDNumber="1"))
            resp = self.mockClient.post("/removeUser/", {"InputUser": "1"})
            checkUser = list(MyUser.objects.filter(IDNumber="1"))
            if ((checkUser.__len__() ==0)):
                self.assertNotEqual("1", checkUser[0].IDNumber, "You removed yourself")
