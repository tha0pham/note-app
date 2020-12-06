class User():
    id = 0
    firstname = ''
    lastname = ''
    email = ''
    password = ''

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
