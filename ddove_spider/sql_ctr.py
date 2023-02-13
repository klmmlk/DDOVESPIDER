import sqlite3

sqldata = sqlite3.connect('data')
cursor = sqldata.cursor()

print('成功连接数据库')


class MySql(object):
    @classmethod
    def insert_db(cls, item):
        sql = "insert into ddove_table(url_id,title,pic_url,dl_url) values (?,?,?,?)"
        values = (item["url_id"], item["title"], str(item["pic_url"]), str(item["dl_url"]))
        cursor.execute(sql, values)
        sqldata.commit()

    @classmethod
    def search_db(cls, item):
        sql = "select url_id from ddove_table where url_id = '%s'" % item
        return cursor.execute(sql).fetchone()


if __name__ == '__main__':
    # item = {
    #     "url_id":'qqq111',
    #     "title":'大中国',
    #     "pic_url":str(['123123','sdfsdf']),
    #     "dl_url":'www.bbbd.com'
    # }
    # MySql.insert_db(item)
    ooo =MySql.search_db('a63742bf4cb304d1')
    print('a63742bf4cb304d1' in ooo)
