from django.test import TestCase
import TAScheduler.classes.Skills as SkillMethods
from TAScheduler.models import MyUser, Skills, UserSkills

class addSkillsTests(TestCase):
    def setUp(self):
        tempSkill = Skills(SkillID="temp name",
                           SkillDescription="temp description")
        tempSkill.save()
    def testPositiveWithDescription(self):
        SkillMethods.SkillsClass.newSkill(self, "testSkill", "testDescription")
        CheckSkill = Skills.objects.filter(SkillID="testSkill")
        self.assertEqual("testSkill",CheckSkill[0].SkillID)
    def testPositiveNoDescription(self):
        SkillMethods.SkillsClass.newSkill(self, "testSkill1", "")
        CheckSkill = Skills.objects.filter(SkillID="testSkill1")
        self.assertEqual("testSkill1", CheckSkill[0].SkillID)

        SkillMethods.SkillsClass.newSkill(self, "testSkill2", None)
        CheckSkill = Skills.objects.filter(SkillID="testSkill2")
        self.assertEqual("testSkill2", CheckSkill[0].SkillID)
    def testNegativeTooManyFields(self):
        with self.assertRaises(TypeError, msg="Should not accept that many fields"):
            SkillMethods.SkillsClass.newSkill(self,"testSkill3", "testDescription", "error")
    def testNegativeTooFewFields(self):
        with self.assertRaises(TypeError, msg="Should not accept that few fields"):
            SkillMethods.SkillsClass.newSkill(self, "testSkill3")
    def testNegativeSkillAlreadyExists(self):
        with self.assertRaises(RuntimeError, msg="Skill already exists"):
            SkillMethods.SkillsClass.newSkill(self, "temp name","new Description")
            CheckSkill = Skills.objects.filter(SkillID="temp name")
            self.assertEqual("temp description", CheckSkill[0].SkillDescription)
class testRemoveSkills(TestCase):
    def setUp(self):
        tempSkill = Skills(SkillID="temp name",
                           SkillDescription="temp description")
        tempSkill.save()
    def testPositiveRemoveSkill(self):
        SkillMethods.SkillsClass.removeSkill(self,"temp name")
        CheckSkill = Skills.objects.filter(SkillID="temp name")
        self.assertEqual(CheckSkill.exists(), False, "Should not have anything to return")
    def testNegativeTooManyFields(self):
        with self.assertRaises(TypeError, msg="Should not accept that many fields"):
            SkillMethods.SkillsClass.newSkill(self, "testSkill3", "error")
    def testNegativeTooFewFields(self):
        with self.assertRaises(TypeError, msg="Should not accept that few fields"):
            SkillMethods.SkillsClass.newSkill(self)
    def testNegativeNoSuchSkill(self):
        with self.assertRaises(RuntimeError, msg="Skill does not exist"):
            SkillMethods.SkillsClass.removeSkill(self, "no name")
            CheckSkill = Skills.objects.filter(SkillID= "no name")
            self.assertEqual(CheckSkill.exists(), False, "Should not have anything to return")
class testAssignNewSkill(TestCase):
    def setUp(self):
        tempSkill = Skills(SkillID="temp name",
                           SkillDescription="temp description")
        tempSkill.save()
        tempUser1 = MyUser(IDNumber="1",
                          name="test",
                          address="test land",
                          email="test@uwm.edu",
                          phoneNumber="123",
                          role="TA",
                          password="1234")
        tempUser1.save()
        tempUser2 = MyUser(IDNumber="2",
                          name="test",
                          address="test land",
                          email="test@uwm.edu",
                          phoneNumber="123",
                          role="Instructor",
                          password="1234")
        tempUser2.save()
        tempAssignment = UserSkills(UserSkillID = "3",
                                    SkillID = tempSkill,
                                    UserID = tempUser1)
        tempAssignment.save()
    def testPositiveAssignSkill(self):
        SkillMethods.SkillsClass.assignNewSkill(self,"4","1","temp name")
        CheckAssignment = UserSkills.objects.filter(UserSkillID="3")
        self.assertEqual(CheckAssignment[0].UserSkillID, "3", "Should return new skill")
    def testNegativeTooManyFields(self):
        with self.assertRaises(TypeError, msg="Should not accept that many fields"):
            SkillMethods.SkillsClass.assignNewSkill(self, "ID1", "User ID", "Skill ID", "error")
    def testNegativeTooFewFields(self):
        with self.assertRaises(TypeError, msg="Should not accept that few fields"):
            SkillMethods.SkillsClass.assignNewSkill(self, "ID2")
    def testNegativeNoSuchUser(self):
        with self.assertRaises(RuntimeError, msg="Should not accept a user that does not exists"):
            SkillMethods.SkillsClass.assignNewSkill(self, "ID3", "4", "temp name")
    def testNegativeNoSuchSkill(self):
        with self.assertRaises(RuntimeError, msg="Should not accept a skill that does not exists"):
            SkillMethods.SkillsClass.assignNewSkill(self, "ID4", "1", "not a real skill")
    def testNegativeNotTA(self):
        with self.assertRaises(RuntimeError, msg="Should not accept a user that is not a TA"):
            SkillMethods.SkillsClass.assignNewSkill(self, "ID5", "2", "temp name")
    def testNegativeAlreadyAssigned(self):
        with self.assertRaises(RuntimeError, msg="Should not try to add a skill assignment that already exists"):
            SkillMethods.SkillsClass.assignNewSkill(self, "3", "1", "temp name")
class testRemoveSkillAssignment(TestCase):
    def setUp(self):
        tempSkill = Skills(SkillID="temp name",
                           SkillDescription="temp description")
        tempSkill.save()
        tempUser = MyUser(IDNumber="1",
                          name="test",
                          address="test land",
                          email="test@uwm.edu",
                          phoneNumber="123",
                          role="TA",
                          password="1234")
        tempUser.save()
        tempAssignment = UserSkills(UserSkillID = "2",
                                    SkillID =tempSkill,
                                    UserID =tempUser)
        tempAssignment.save()
    def testPositiveSkillRemoval(self):
        SkillMethods.SkillsClass.removeSkillAssignment(self,"2")
        checkAssignment = UserSkills.objects.filter(UserSkillID="2")
        self.assertEqual(checkAssignment.exists(), False, "Should not have anything to return")
    def testNegativeTooManyFields(self):
        with self.assertRaises(TypeError, msg="Should not accept that many fields"):
            SkillMethods.SkillsClass.removeSkillAssignment(self,"2", "error")

    def testNegativeTooFewFields(self):
        with self.assertRaises(TypeError, msg="Should not accept that few fields"):
            SkillMethods.SkillsClass.removeSkillAssignment(self)
    def testNegativeNoSuchAssignment(self):
        with self.assertRaises(RuntimeError, msg="No Such assignment to remove"):
            SkillMethods.SkillsClass.removeSkillAssignment(self, "3")
            checkAssignment = UserSkills.objects.filter(UserSkillID="2")
            self.assertEqual(checkAssignment.exists(), True, "Should not remove 2")
            checkAssignment = UserSkills.objects.filter(UserSkillID="3")
            self.assertEqual(checkAssignment.exists(), False, "Should not add 3")
