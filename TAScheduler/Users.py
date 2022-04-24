from .models import MyUser


class UserClass():

    def createUser(self, IdNumber, name, address, email, phoneNumber, role, password):
        check = list(map(str, MyUser.objects.filter(userID=IdNumber)))
        if len(check) > 0:
            raise Exception("Database already contains someone with that ID")
        else:
            temp = MyUser(userID=IdNumber, name=name, address=address, email=email, phoneNumber=phoneNumber, role=role,
                          password=password)
            temp.save()
