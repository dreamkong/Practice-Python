import pymysql


class MysqlSearch(object):

    def get_conn(self):
        # 获取连接
        try:
            self.conn = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='root',
                db='wangyi_news',
                port=3306,
                charset='utf8'
            )
        except pymysql.Error as e:
            print(e)

    def close_conn(self):
        try:
            if self.conn:
                # 关闭连接
                self.conn.close()
        except pymysql.Error as e:
            print(e)

    def get_one(self):
        self.get_conn()
        # 找到sql
        sql = 'SELECT * FROM news WHERE types = %s ORDER BY created_at DESC'
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行sql
        cursor.execute(sql, ('惊悚'))
        # 拿到结果
        result = dict(zip([description[0]
                           for description in cursor.description], cursor.fetchone()))
        # 处理数据
        # 关闭cursor
        self.conn.close()
        return result

    def get_more(self):
        self.get_conn()
        # 找到sql
        sql = 'SELECT * FROM news WHERE types != %s ORDER BY created_at DESC'
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行sql
        cursor.execute(sql, ('惊悚'))
        # 拿到结果
        result = [dict(zip([description[0]
                            for description in cursor.description], row))for row in cursor.fetchall()]
        # 处理数据
        # 关闭cursor
        self.conn.close()
        return result

    def add_one(self):
        try:
            self.get_conn()
            # 获取sql
            sql = 'INSERT INTO news(title, content, types, image, author, view_count, created_at, is_valid) VALUES(%s, %s, %s, %s, %s, %s, now(), %s)'
            # 获取连接和cursor
            cursor = self.conn.cursor()
            # 提交数据到数据库
            cursor.execute(sql, ('我是标题', '我是内容', '我是types',
                                 '我是图片', '我是作者', 666, 1))
            # 提交事务
            self.conn.commit()
            # 关闭cursor和连接
            cursor.close()
            
        except pymysql.Error as e:
            print(e)
            self.conn.rollback()
        self.close_conn()

def main():
    obj = MysqlSearch()
    # obj.get_one()
    # obj.add_one()
    for item in obj.get_more():
        print(item)


if __name__ == '__main__':
    main()
