from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)
# mysql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/wangyi_news?charset=utf8'
# mongodb
app.config['MONGODB_SETTINGS'] = {
    'db': 'mongo_news',
    'host': 'localhost',
    'port': 27017
}
# SQLAlchemy
# db = SQLAlchemy(app)
# MongoEngine
db = MongoEngine(app)


# class News(db.Model):
#     __tablename__ = 'news'

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     content = db.Column(db.String(2000), nullable=False)
#     types = db.Column(db.String(10), nullable=False)
#     image = db.Column(db.String(300))
#     author = db.Column(db.String(20))
#     view_count = db.Column(db.Integer)
#     created_at = db.Column(db.DATETIME)
#     is_valid = db.Column(db.Boolean)

#     def __repr__(self):
#         return '<News %r> ' % self.title

class News(db.Document):
    title = db.StringField(max_length=200, required=True)
    content = db.StringField(required=True)
    types = db.StringField(requiresd=True)
    image = db.StringField()
    is_valid = db.BooleanField(default=True)
    created_at = db.DateTimeField(default=datetime.now())
    updated_at = db.DateTimeField(default=datetime.now())

    meta = {
        'collection': 'news',
        'ordering': ['-created_at']
    }


def add_data():
    new_obj = News(
        title='惊现UFO！',
        content='我是新闻内容',
        types='推荐',
        image='http://www.chinanews.com/yl/yl-ypkb/news/2009/07-31/U149P4T8D1799129F107DT20090731133550.jpg',
    )
    new_obj.save()
    return new_obj


@app.route('/')
def index():
    # news_list = News.query.all()
    news_list = News.objects.all()
    return render_template('index.html', news_list=news_list)


@app.route('/cat/<name>/')
def cat(name):
    # news_list = News.query.filter(News.types == name)
    news_list = News.objects.filter(types=name)
    return render_template('cat.html', name=name, news_list=news_list)


@app.route('/detail/<pk>/')
def detail(pk):
    # news = News.query.get(pk)
    news = News.objects.filter(pk=pk).first_or_404()
    return render_template('detail.html', news=news)


@app.route('/date')
def rest():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    app.run(debug=True)
