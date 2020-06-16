import pymysql

class Mysql_client(object):
    def __init__(self):
        # 打开数据库
        self.db = pymysql.connect("localhost", "root", "root", "testpachong1")
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()
    def  insert_db(self,items):
        count = 0
        for item in items:
            # sql 语句动态化
            sql = "INSERT INTO test_job(job_name, \
                   company_name, company_address,money,date) \
                   VALUES ('%s', '%s','%s','%s','%s')" % \
                  (item['job_name'], item['company_name'], item['company_address'], item['money'], item['date'])
            try:
                # 执行sql
                self.cursor.execute(sql)
                self.db.commit()
                count = count + 1
            except:
                self.db.rollback()
        print("已成功插入" + str(count) + "条数据")

    def close_db(self):
        self.db.close()
insert_data = Mysql_client()