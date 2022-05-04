from TAScheduler.models import MyUser, Sections, Course


class SectionsClass():

    def createSection(self, SectionCode, ParentID):
        if (SectionCode is None):
            raise Exception("does not accept null Primary keys")
        checkRepeat = list(map(str, Sections.objects.filter(sectionCode=SectionCode)))
        checkParent = Course.objects.filter(courseCode=ParentID)
        if checkParent.count() == 0:
            raise Exception("No such parent course")
        if len(checkRepeat) != 0:
            raise Exception("Database already contains a section with that ID")
        else:
            x = Course.objects.get(courseCode=ParentID)
            temp = Sections(sectionCode=SectionCode, parentCode=x ,TA= None)
            temp.save()

    def assignTAsec(self, SectionCode, TAcode):
        toUpdate = Sections.objects.get(sectionCode=SectionCode)
        taCode = MyUser.objects.get(IDNumber=TAcode)
        toUpdate.TA = taCode
        toUpdate.save()

    def removeTAsec(self, SectionCode, TAcode):
        toUpdate = Sections.objects.get(sectionCode=SectionCode)
        toUpdate.TA = None
        toUpdate.save()
