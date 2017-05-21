from werkzeug.security import check_password_hash

class User():

    def __init__(self,username, password, email, name, lastname, imgurl, desc):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.lastname= lastname
        self.imgurl = imgurl
        self.desc = desc
        

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
