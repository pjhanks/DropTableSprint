from .models import MyUser
class Users():
  
  def createUser(self, IdNumber, name, address, email, phoneNumber, role):
    check = list(map(str, MyUser.objects.filter(ID=IdNumber)))
    if len(check)==0:
      raise Exception("Database already contains someone with that ID")
    else:
      temp = MyUser(IdNumber, name, address, email, phoneNumber, role)
      temp.save