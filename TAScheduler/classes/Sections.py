from TAScheduler.models import Sections, Course, MyUser, ClassTAAssignments


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
        courseCode = toUpdate.parentCode
        sectionCode = toUpdate.sectionCode
        check = Sections.objects.filter(sectionCode=sectionCode, TA=taCode)
        if check.count()>0:
            raise RuntimeError("A TA is already assigned to that section!")
        else:
            # temp = Sections(sectionCode=SectionCode, parentCode=courseCode, TA=taCode)
            # temp.save()
            toUpdate.TA = taCode
            toUpdate.save()
            # toUpdate.TA = taCode
            # toUpdate.save()

    def removeTAsec(self, SectionCode, TAcode):
        sectionCode = Sections.objects.get(sectionCode=SectionCode)
        parentCode = sectionCode.parentCode
        taCode = MyUser.objects.get(IDNumber=TAcode)
        try:
            toUpdate = Sections.objects.get(sectionCode=sectionCode, parentCode=parentCode)
            if toUpdate.TA.IDNumber != TAcode:
                raise RuntimeError("That TA isn't assigned to that course!")
            else:
                print(toUpdate)
                toUpdate.TA = None
                toUpdate.save()
        except Exception:
            print("No Section object exists")

