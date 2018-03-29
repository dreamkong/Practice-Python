
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DATETIME, Boolean
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'mysql+pymysql://root:root@localhost:3306/wangyi_news?charset=utf8')
Base = declarative_base()

Session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(2000), nullable=False)
    types = Column(String(10), nullable=False)
    image = Column(String(300))
    author = Column(String(20))
    view_count = Column(Integer)
    created_at = Column(DATETIME)
    is_valid = Column(Boolean)


class OrmTest(object):

    def __init__(self):
        self.session = Session()

    def add_one(self):
        # 新增记录
        new_obj = News(
            title='orm标题',
            content='orm内容',
            types='orm types'
        )
        self.session.add(new_obj)
        self.session.commit()
        return new_obj

    def get_one(self):
        return self.session.query(News).get(1)

    def get_more(self):
        return self.session.query(News).filter_by(is_valid=True, title='我是标题')

    def delete_data(self):
        obj = self.session.query(News).get(1)
        if obj:
            self.session.delete(obj)
            self.session.commit()

    def update_data(self):
        obj = self.session.query(News).get(1)
        if obj:
            obj.title = '我改了标题'
            self.session.add(obj)
            self.session.commit()
        return obj


def main():
    obj = OrmTest()
    # rest = obj.get_more()
    # for i in rest:
    #     print(i.title)
    # print(rest.count())
    # rest = obj.update_data()
    # print(rest.title)
    obj.delete_data()


if __name__ == '__main__':
    main()
