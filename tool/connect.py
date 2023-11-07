import pymysql

conn = pymysql.connect(host='localhost', user='root', password='qjw123456', db='mail')
cursor = conn.cursor(pymysql.cursors.DictCursor)


# 查询数据
def query(date_value):
    try:
        sql = f"SELECT * FROM taskMail WHERE Date = '{date_value}';"
        cursor.execute(sql)
        res = cursor.fetchall()
    except pymysql.Error as e:
        print(f"错误：{e}")
        res = []
    finally:
        cursor.close()
    return res


# 插入数据
def insert(table, data):
    try:
        sql = "INSERT INTO {} ({}) VALUES ({})".format(table, ','.join(data.keys()), ','.join(['%s'] * len(data)))
        cursor.execute(sql, list(data.values()))
        conn.commit()
        return True  # 插入成功，返回True
    except pymysql.Error as e:
        conn.rollback()
        print(f"错误：{e}")
        return False  # 插入失败，返回False
    finally:
        cursor.close()
        conn.close()
