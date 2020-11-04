import pymysql

class MySql():
    #Mysql数据库的连接信息，包括IP地址、用户名、密码、端口号、数据库名称
    def __init__(self,host = '127.0.0.1', username = 'root', password = 'root', port = 3306, database = 'db'):
        self.connect = pymysql.connect(
            host = host,
            port = port,
            user = username,
            password = password,
            database = database,
            charset = 'utf8'
        )
        self.cursor = self.connect.cursor()    
    #Mysql数据库连接的关闭，在查询结束后应该关闭数据库连接
    def close(self):
        self.connect.close()
    #Mysql数据库的查询操作，将根据 sqlStr变量中的查询语句进行查询
    def query(self, sqlStr):
        #执行异常处理语句
        try:
            #Mysqld对象游标执行查询语句
            self.cursor.execute(sqlStr)
            #获取所有的查询列表，返回一个行列表
            rows = self.cursor.fetchall()
            return rows
        #如何出现异常返回异常
        except Exception as e:
            print (e)
            return None

if __name__ == "__main__":
    MySql()