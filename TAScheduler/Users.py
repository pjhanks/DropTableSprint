from .models import MyUser


class UserClass():

    def createUser(self, IdNumber, name, address, email, phoneNumber, role, password):
        if (IdNumber is None):
            raise Exception("does not accept null Primary keys")
        if (not((role == "Instructor") or (role == "TA") or (role == "Instructor"))):
            raise Exception("Invalid Role")
        check = list(map(str, MyUser.objects.filter(IDNumber=IdNumber)))
        if len(check) > 0:
            raise Exception("Database already contains someone with that ID")
        else:
            if (isinstance(IdNumber, str) and isinstance(name, str) and isinstance(address, str) and isinstance(email,
                                                                                                                str) and isinstance(
                phoneNumber, str) and isinstance(role, str) and isinstance(password, str)):
                temp = MyUser(IdNumber, name, address, email, phoneNumber, role, password)
                temp.save()
            else:
                raise Exception("wrong input")
