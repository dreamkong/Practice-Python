from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/wangyi_news?charset=utf8'
db = SQLAlchemy(app)


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    types = db.Column(db.String(10), nullable=False)
    image = db.Column(db.String(300))
    author = db.Column(db.String(20))
    view_count = db.Column(db.Integer)
    created_at = db.Column(db.DATETIME)
    is_valid = db.Column(db.Boolean)

    def __repr__(self):
        return '<News %r> ' % self.title


@app.route('/')
def index():
    news_list = News.query.all()
    return render_template('index.html', news_list=news_list)


@app.route('/cat/<name>/')
def cat(name):
    news_list = News.query.filter(News.types == name)
    return render_template('cat.html', name=name, news_list=news_list)


@app.route('/detail/<int:pk>/')
def detail(pk):
    news = News.query.get(pk)
    return render_template('detail.html', news=news)


@app.route('/date')
def rest():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    app.run(debug=True)
