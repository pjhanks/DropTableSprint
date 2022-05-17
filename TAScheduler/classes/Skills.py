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
        checkUser = MyUser.objects.filter(IDNumber = userId)

        if not checkUser.exists():
            raise RuntimeError("User does not exist")
            return
        if checkUser[0].role!="TA":
            raise RuntimeError("User is not a TA")
        checkSkill = Skills.objects.filter(SkillID = skillName)
        if not checkSkill.exists():
            raise RuntimeError("Skill does not exist")
            return
        checkAssignment= UserSkills.objects.filter(UserSkillID=userSkillID)
        if checkAssignment.exists():
            raise RuntimeError("Assignment Id in use")
            return
        checkSkillAsignment = UserSkills.objects.filter(SkillID=skillName)
        for a in checkSkillAsignment:
            if a.UserID == userId:
                raise RuntimeError("Already have that skill")
        skillAsignment = UserSkills(userSkillID,skillName, userId )
        skillAsignment.save()

    def removeSkillAssignment(self, userSkillID):
        check = UserSkills.objects.filter(UserSkillID=userSkillID)
        if not check.exists():
            raise RuntimeError("User skill assignment does not exist")
        else:
            check[0].delete()