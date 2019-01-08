import pymysql.cursors
import pymysql
import datetime

class xiemysql:
    def __init__(self,host,port,user,password, dbs, charset ,cursorclass):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbs = dbs
        self.charset = charset
        self.cursorclass = cursorclass
    def connections(self):
        connection = pymysql.connect(host=self.host,
                                     port = self.port,
                                     user=self.user,
                                     password =self.password,
                                     db = self.dbs,
                                     charset=self.charset,
                                     cursorclass=self.cursorclass)
        return connection