driver = "{MySQL ODBC 8.0 Unicode Driver}"
srv = "192.168.56.133"
DB = "users"
log = "user123"
pwd = "Qazwsx123"
timers = [5, 10, 20, 30]


class User:
    def __init__(self, name, mail, msg=1, birthday=0, send=0):
        self.name = name
        self.mail = mail
        self.msg = msg
        self.birthday = birthday
        self.send = send

    def __str__(self):
        return self.mail
