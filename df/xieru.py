

import pymysql.cursors
import pymysql
from df.mysqlxie import xiemysql

my_connection = xiemysql('58edd9c77adb6.bj.cdb.myqcloud.com',
                        5432, 'root', '1160329981wang', 'qianmancang', 'utf8mb4', pymysql.cursors.DictCursor)
connection = my_connection.connections()
class mysql_xie:
    def __init__(self,name,code,gainian,date):
        self.name = name
        self.code = code
        self.gainian = gainian
        self.date = date

    def xie_gainian(self):
        try:
            with connection.cursor() as cursor:

                # 执行sql语句，插入记录
                SQL = """insert into gainian(name,code,gainian,date)
                values
                (%s, %s, %s, %s)"""
                cursor.execute(SQL, (self.name, self.code, self.gainian, self.date))
                # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                connection.commit()
        except Exception as e:
            print('***** Logging failed with this error:', str(e))