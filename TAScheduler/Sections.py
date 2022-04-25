from .models import Sections, Course


class SectionsClass():

    def createSection(self, SectionCode, ParentID):
        if (SectionCode is None):
            raise Exception("does not accept null Primary keys")
        checkRepeat = list(map(str, Sections.objects.filter(sectionCode=SectionCode)))
        checkParent = list(map(str, Sections.objects.filter(courseCode=ParentID)))
        if len(checkParent == 0):
            raise Exception("No such parent course")
        if len(checkRepeat) != 0:
            raise Exception("Database already contains am course with that ID")
        else:
            temp = Sections(SectionCode, ParentID, None)
            temp.save()
