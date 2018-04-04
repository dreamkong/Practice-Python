from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId


class TestMongo(object):

    def __init__(self):
        self.client = MongoClient('localhost')
        self.db = self.client['blog']

    def add_one(self):
        post = {
            'title': '新的标题',
            'content': '新的内容',
            'created_at': datetime.now()
        }
        return self.db.posts.insert_one(post)

    def add_many(self):
        posts = [{
            'title': '标题',
            'content': '内容',
            'created_at': datetime.now()
        } for i in range(10)]
        return self.db.posts.insert_many(posts)

    def get_one(self):
        '''查询一条数据'''
        return self.db.posts.find_one()

    def get_many(self):
        '''查询多条数据'''
        return self.db.posts.find()

    def get_one_from_oid(self, oid):
        '''根据记录的ID查询数据'''
        return self.db.posts.find_one({'_id': ObjectId(oid)})

    def update_one(self):
        return self.db.posts.update_one({'title': '新的标题'}, {'$set': {'content': '我是更新的内容one'}})

    def update_many(self):
        return self.db.posts.update_many({'title': '标题'}, {'$set': {'content': '我是更新的内容many'}})

    def delete_one(self):
        return self.db.posts.delete_one({'title': '新的标题'})

    def delete_many(self):
        return self.db.posts.delete_many({'title': '标题', 'content': '内容'})


def main():
    obj = TestMongo()
    # rest = obj.add_one()
    # rest = obj.add_many()
    # rest = obj.get_many()
    # for r in rest:
    #     print(r)
    # rest = obj.get_one_from_oid('5ac48cca74328e35449b0ec4')
    # rest = obj.update_many()
    # print(rest.matched_count)
    # print(rest.modified_count)
    rest = obj.delete_many()
    print(rest.deleted_count)
    print(rest)


if __name__ == '__main__':
    main()
