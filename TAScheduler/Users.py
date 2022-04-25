from .models import MyUser


class UserClass():

    def createUser(self, IdNumber, name, address, email, phoneNumber, role, password):
        check = list(map(str, MyUser.objects.filter(IDNumber=IdNumber)))
        if len(check) > 0:
            raise Exception("Database already contains someone with that ID")
        elif type(IdNumber) != str or type(name) != str or type(address) != str or type(email) != str or \
            type(phoneNumber) != str or type(role) != str or type(password) != str:
            raise TypeError("You must pass str values for all of the user paramters!")
        else:
            temp = MyUser(IDNumber=IdNumber, name=name, address=address, email=email, phoneNumber=phoneNumber, role=role,
                          password=password)
            temp.save()
