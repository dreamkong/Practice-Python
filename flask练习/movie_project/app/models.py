"""
Created by dreamkong on 2018/10/31
"""
from datetime import datetime

from flask import Flask
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, SmallInteger, BigInteger, Date

from app import bcrypt, db

__author__ = 'dreamkong'


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(30))
    email = Column(String(100), unique=True)
    phone = Column(String(11), unique=True)
    info = Column(Text)
    avatar = Column(String(100), comment='头像')
    add_time = Column(DateTime, index=True, default=datetime.now())
    uuid = Column(String(255), unique=True, comment='唯一标志符')
    user_log = db.relationship('UserLog', backref='user')  # 会员日志外键关系关联
    comment = db.relationship('Comment', backref='user')
    movie_fav = db.relationship('MovieFav', backref='user')

    def __repr__(self):
        return '<User {}>'.format(self.name)


class UserLog(db.Model):
    __tablename__ = 'user_log'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    ip = Column(String(100))
    add_time = Column(DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<UserLog {}>'.format(self.id)


class Tag(db.Model):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    add_time = Column(DateTime, index=True, default=datetime.now)
    movies = db.relationship('Movie', backref='tag')  # 电影外键关系关联

    def __repr__(self):
        return '<Tag {}>'.format(self.name)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True)
    url = Column(String(255), unique=True)
    info = Column(Text)
    logo = Column(String(255))
    star = Column(SmallInteger)
    play_nums = Column(BigInteger)
    comment_nums = Column(BigInteger)
    tag_id = Column(Integer, ForeignKey('tag.id'))
    area = Column(String(255))
    release_time = Column(Date)
    length = Column(String(50))
    add_time = Column(DateTime, index=True, default=datetime.now)
    comment = db.relationship('Comment', backref='movie')
    movie_fav = db.relationship('MovieFav', backref='movie')

    def __repr__(self):
        return '<Movie {}>'.format(self.title)


# 上映预告
class Preview(db.Model):
    __tablename__ = 'preview'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True)
    logo = Column(String(255))
    add_time = Column(DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Preview {}>'.format(self.title)


# 评论
class Comment(db.Model):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    movie_id = Column(Integer, ForeignKey('movie.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    add_time = Column(DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Comment {}>'.format(self.id)


# 电影收藏
class MovieFav(db.Model):
    __tablename__ = 'movie_fav'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    add_time = Column(DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<MovieFav {}>'.format(self.id)


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Auth {}>".format(self.name)


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 角色权限列表
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admins = db.relationship("Admin", backref='role')  # 管理员外键关系关联

    def __repr__(self):
        return "<Role {}>".format(self.name)


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    password = db.Column(db.String(100))  # 管理员密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员，0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admin_logs = db.relationship("AdminLog", backref='admin')  # 管理员登录日志外键关系关联
    operate_logs = db.relationship("OperateLog", backref='admin')  # 管理员操作日志外键关系关联

    def __repr__(self):
        return "<Admin {}>".format(self.name)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


# 管理员登录日志
class AdminLog(db.Model):
    __tablename__ = "admin_log"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<AdminLog {}>".format(self.id)


# 操作日志
class OperateLog(db.Model):
    __tablename__ = "operate_log"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 操作IP
    reason = db.Column(db.String(600))  # 操作原因
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<OperateLog {}>".format(self.id)


if __name__ == '__main__':
    app = Flask(__name__)
    app.app_context().push()
    app.config.from_object('app.config')
    db.init_app(app)
    db.create_all(app=app)
    role = Role(
        name='超级管理员',
        auths=''
    )
    db.session.add(role)
    from flask_bcrypt import Bcrypt as Bcrypt2
    bcrypt2 = Bcrypt2()
    bcrypt2.init_app(app)
    admin = Admin(
        name='admin',
        password=bcrypt2.generate_password_hash('admin'),
        is_super=0,
        role_id=1
    )
    db.session.add(admin)
    db.session.commit()
