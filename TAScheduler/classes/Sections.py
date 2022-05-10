from TAScheduler.models import Sections, Course


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
