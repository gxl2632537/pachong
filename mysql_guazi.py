import pymysql

class Mysql_client(object):
    def __init__(self):
        # 打开数据库
        self.db = pymysql.connect("localhost", "root", "root", "testpachong1")
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    def insert_db(self,items):
        count = 0
        for i in items:
            # print(items)
            # sql 语句动态化
            sql = "INSERT INTO guazi_data(car_id, \
                    car_name, from_url,car_price,license_time,km_info,license_location,desplacement_info,transmission_case,mian_picture_url) \
                    VALUES ('%s', '%s','%s','%s','%s', '%s','%s','%s','%s','%s')" % \
                  (i['car_id'], i['car_name'], i['from_url'], i['car_price'], i['license_time'], i['km_info'], i['license_location'], i['desplacement_info'], i['transmission_case'], i['mian_picture_url'])
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

    def get_task(self,item):
        # SQL 查询语句
        sql = "SELECT * FROM guazi_task \
               WHERE id = %s" % (item)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            # 找到一个数据并且删除,取出的task不重复
            self.del_db(item)
            for row in results:
                task_url = row[1]
                city_name = row[2]
                brand_name = row[3]
                item_type = row[4]

            list = {'task_url':task_url,'city_name':city_name,'brand_name':brand_name,'item_type':item_type,}

            return list
                # 打印结果
                # print("task_url=%s,city_name=%s,brand_name=%s,item_type=%s" % \
                #       (task_url, city_name, brand_name, item_type))
        except:
            print("Error: unable to fetch data")

    def del_db(self,item):
        # SQL 删除语句
        sql = "DELETE FROM guazi_task WHERE id = %s" % (item)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交修改
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()

insert_data = Mysql_client()