from TAScheduler.models import Skills, MyUser, UserSkills

class SkillsClass():
    def newSkill(self, skillName, skillDescription):
        check = Skills.objects.filter(SkillID=skillName)
        if check.exists():
            raise RuntimeError("Database already contains that skill")
        skillToAdd = Skills(skillName, skillDescription)
        skillToAdd.save()

    def removeSkill(self, skillName):
        check = Skills.objects.filter(SkillID=skillName)
        if not check.exists():
            raise RuntimeError("Database does not contain that skill")
        else:
            check[0].delete()
    def assignNewSkill(self, userSkillID,userId, skillName):
        check = MyUser.objects.filter(IDNumber = userId)
        if not check.exists():
            raise RuntimeError("User does not exist")
            return
        check2 = Skills.objects.filter(SkillID = skillName)
        if not check2.exists():
            raise RuntimeError("Skill does not exist")
            return

        check = UserSkills.objects.filter(SkillID=skillName)
        for a in check:
            if a.SkillID == skillName:
                raise RuntimeError("Already have that skill")
        skillAsignment = UserSkills(userSkillID,skillName, userId )
        skillAsignment.save()

    def removeSkillAssignment(self, userSkillID):
        check = UserSkills.objects.filter(UserSkillID=userSkillID)
        if not check.exists():
            raise RuntimeError("User skill assignment does not exist")
        else:
            check[0].delete()