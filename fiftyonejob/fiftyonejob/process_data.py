# -*- coding: utf-8 -*-
import json
import redis  # pip install redis
import pymysql

def main():
    # 指定redis数据库信息
    rediscli = redis.StrictRedis(host='39.108.217.147', port = 6379, db = 0)
    # 指定mysql数据库
    mysqlcli = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='temp', charset='utf8',)

    # 无限循环
    while True:
        source, data = rediscli.blpop(["fifty:items"]) # 从redis里提取数据

        item = json.loads(data.decode('utf-8')) # 把 json转字典

        try:
            # 使用cursor()方法获取操作游标
            cur = mysqlcli.cursor()
            # 使用execute方法执行SQL INSERT语句
            sql =  'insert into job(url,enterprise_name,pname,smoney,emoney,plocation,experience,position_education,ptype,tags,date_pub,advantage,jobdesc,parea,pnumber,company_profile,crawl_time) ' \
              'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update ' \
              'pname=values(pname),smoney=VALUES(smoney),emoney=VALUES(emoney), plocation=VALUES(plocation), experience=VALUES(experience), ' \
                'position_education=VALUES(position_education), ptype=VALUES(ptype), tags=VALUES(tags), date_pub=VALUES(date_pub), advantage=VALUES(advantage), ' \
                   'jobdesc=VALUES(jobdesc), parea=VALUES(parea), pnumber=VALUES(pnumber),crawl_time=VALUES(crawl_time)'

            cur.execute(sql, (
                item['url'],item['enterprise_name'],item['pname'],item['smoney'],item['emoney'],item['plocation'],
                item['experience'],item['position_education'],item['ptype'],item['tags'],item['date_pub'],item['advantage'],item['jobdesc'],
                item['parea'],item['pnumber'],item['company_profile'],item['crawl_time']
            ))

            # 提交sql事务
            mysqlcli.commit()
            #关闭本次操作
            cur.close()
            print ("插入 %s" % item['pname'])
        except pymysql.Error as e:
            mysqlcli.rollback()
            print ("插入错误" ,str(e))

if __name__ == '__main__':
    main()