from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

client = MongoClient(os.getenv('mongo'))
try:
    # The ping command is cheap and does not require auth.
    client.admin.command('ping')
    status = True
    mydb = client['znzup']
    table = mydb['ddove']
except ConnectionFailure:
    print("连接数据库失败")
    status = False


class Mongo:
    @classmethod
    def insert_one(cls, items: dict):
        if status:
            return table.insert_one(items)
        else:
            return False


if __name__ == '__main__':
    pass
