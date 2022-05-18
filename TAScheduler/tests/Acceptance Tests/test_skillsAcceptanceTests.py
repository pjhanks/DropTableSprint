from django.test import TestCase, Client
from TAScheduler.models import MyUser, Skills, UserSkills

class SkillsTests(TestCase):
    def setUp(self):
        self.mockClient = Client()
        TA = MyUser(IDNumber="1",
                      name="Alex",
                      address="124 park place",
                      email="alex@uwm.edu",
                      phoneNumber="18000000001",
                      role="TA",
                      password="123");
        TA.save()
        Super = MyUser(IDNumber="2",
                      name="Alex",
                      address="124 park place",
                      email="alex@uwm.edu",
                      phoneNumber="18000000001",
                      role="Supervisor",
                      password="123")
        Super.save()
        Teach = MyUser(IDNumber="2",
                       name="Alex",
                       address="124 park place",
                       email="alex@uwm.edu",
                       phoneNumber="18000000001",
                       role="Instructor",
                       password="123")
        Teach.save()
        Skill = Skills(SkillID="1",
                       SkillDescription="Test")
        Skill.save()
        Skill2 = Skill(SkillID="2",
                       SkillDescription="Test2")
        Skill2.save()
        SkillAssignment =  UserSkills(UserSkillID="2",
                                      SkillID=Skill,
                                      UserID=TA)
        SkillAssignment.save()
        self.mockClient.post("/", {"InputUsername": "2", "InputPassword": "123"}, follow=True)

    def _testNewSkill(self):
        resp = self.mockClient.post("/userTemplates/addSkillSup/", {"id":"2", "newSkill":"test2"},follow=True)
        checkSkill = Skills.objects.filter(SkillID="2")
        self.assertEqual(True, checkSkill.exists(), "Skill Not added")

    def _testRemoveSkill(self):
        resp = self.mockClient.post("/userTemplates/removeSkill/", {"id":"1", "removedSkill":"Test"},follow=True)
        checkSkill = Skills.objects.filter(SkillID="1")
        self.assertEqual(False, checkSkill.exists(), "Skill Not removed")

    def _testAssignSkill(self):
        self.mockClient.post("/", {"InputUsername": "1", "InputPassword": "123"}, follow=True)
        resp = self.mockClient.post("/serTemplates/addSkills", {"id":"1", "loggedUser":"1", "name":"2"}, follow=True)
        checkSkillAssignment = UserSkills.objects.filter(SkillID="1")
        self.assertEqual(True, checkSkillAssignment.exists(), "Skill Assignment Not added")

    def _testRemoveSkill(self):
        resp = self.mockClient.post("/userTemplates/removeSkillAssign/", {"id":"2", "loggedUser":"1", "name":"1"}, follow=True)
        checkSkill = UserSkills.objects.filter(SkillID="2")
        self.assertEqual(False, checkSkill.exists(), "Skill Assignment Not removed")

    def _testAssignAsInstructor(self):
        self.mockClient.post("/", {"InputUsername": "3", "InputPassword": "123"}, follow=True)
        resp = self.mockClient.post("/serTemplates/addSkills", {"id":"1", "loggedUser":"1", "name":"1"}, follow=True)
        checkSkillAssignment = UserSkills.objects.filter(UserID="1")
        self.assertEqual(False, checkSkillAssignment.exists(), "Skill Assignment should not be added")

    def _testNoSuchSkill(self):
        self.mockClient.post("/", {"InputUsername": "1", "InputPassword": "123"}, follow=True)
        resp = self.mockClient.post("/serTemplates/addSkills", {"id": "1", "loggedUser": "1", "name": "5"}, follow=True)
        checkSkillAssignment = UserSkills.objects.filter(UserID="1")
        self.assertEqual(False, checkSkillAssignment.exists(), "No such skill should be addable")

    def _testNoSuchUser(self):
        resp = self.mockClient.post("/serTemplates/addSkills", {"id": "1", "loggedUser": "4", "name": "5"}, follow=True)
        checkSkillAssignment = UserSkills.objects.filter(UserID="1")
        self.assertEqual(False, checkSkillAssignment.exists(), "No such user exists to have skills")

    def _testAlreadyHasSkill(self):
        self.mockClient.post("/", {"InputUsername": "1", "InputPassword": "123"}, follow=True)
        resp = self.mockClient.post("/serTemplates/addSkills", {"id": "1", "loggedUser": "1", "name": "1"}, follow=True)
        checkSkillAssignment = UserSkills.objects.filter(UserID="1")
        self.assertEqual(1, checkSkillAssignment.__len__(), "Skill Assignment Not added")
