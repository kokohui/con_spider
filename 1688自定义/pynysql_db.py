import pymysql


class DataBaseHandle(object):

    def __init__(self, host, username, password, database, port):

        """初始化数据库信息并创建数据库连接"""

        # 下面的赋值其实可以省略，connect 时 直接使用形参即可
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.db = pymysql.connect(self.host, self.username, self.password, self.database, self.port, charset='utf8')
        self.cursor = ''


    #  这里 注释连接的方法，是为了 实例化对象时，就创建连接。不许要单独处理连接了。
    #
    # def connDataBase(self):
    #     ''' 数据库连接 '''
    #
    #     self.db = pymysql.connect(self.host,self.username,self.password,self.port,self.database)
    #
    #     # self.cursor = self.db.cursor()
    #
    #     return self.db

    def insertDB(self, sql):
        """插入数据库操作"""

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def deleteDB(self, sql):
        """操作数据库数据删除 """
        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 删除数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def updateDb(self, sql):
        """更新数据库操作"""

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 更新数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def selectDb(self, sql):
        """数据库查询"""
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)  # 返回 查询数据 条数 可以根据 返回值 判定处理结果

            data = self.cursor.fetchall()  # 返回所有记录列表

            print(data)

            # 结果遍历
            for row in data:
                sid = row[0]
                name = row[1]
                # 遍历打印结果
                print('sid = %s,  name = %s' % (sid, name))
        except:
            print('Error: unable to fecth data')
        finally:
            self.cursor.close()

    def closeDb(self):
        """数据库连接关闭"""
        self.db.close()

if __name__ == '__main__':

    DbHandle = DataBaseHandle('127.0.0.1','adil','helloyyj','AdilTest',3306)

    DbHandle.insertDB('insert into test(name) values ("%s")'%('FuHongXue'))
    DbHandle.insertDB('insert into test(name) values ("%s")'%('FuHongXue'))
    DbHandle.selectDb('select * from test')
    DbHandle.updateDb('update test set name = "%s" where sid = "%d"' %('YeKai',22))
    DbHandle.selectDb('select * from test')
    DbHandle.insertDB('insert into test(name) values ("%s")'%('LiXunHuan'))
    DbHandle.deleteDB('delete from test where sid > "%d"' %(25))
    DbHandle.selectDb('select * from test')
    DbHandle.closeDb()
