"""
Created by dreamkong on 2018/10/31
"""
import uuid
from datetime import datetime
from functools import wraps

import os
from werkzeug.utils import secure_filename

from app import bcrypt, db
from app.home.forms import RegisterForm, LoginForm, UserDetailForm
from app.models import User, UserLog

# from manage import app

__author__ = 'dreamkong'

from . import home
from flask import render_template, redirect, url_for, flash, request, session, current_app


# def change_filename(filename):
#     fileinfo = os.path.splitext(filename)
#     filename = datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + fileinfo[-1]
#     return filename


# 登录装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@home.route('/', methods=['GET'])
def index():
    return render_template('home/index.html')


@home.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if user.check_password(data['password']):
            flash('密码错误！', 'err')
            return redirect(url_for('home.login'))
        session['user'] = user.name
        session['user_id'] = user.id
        user_log = UserLog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(user_log)
        db.session.commit()
        return redirect(url_for('home.user'))
    return render_template('home/login.html', form=form)


@home.route('/logout/', methods=['GET'])
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('home.login'))


@home.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            password=bcrypt.generate_password_hash(data['password']),
            email=data['email'],
            phone=data['phone'],
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash('注册成功！', 'ok')
    return render_template('home/register.html', form=form)


# @home.route('/user/', methods=['GET', 'POST'])
# @user_login_req
# def user():
#     form = UserDetailForm()
#     user = User.query.get(int(session['user_id']))
#     form.avatar.validators = []
#     if request.method == 'GET':
#         form.name.data = user.name
#         form.email.data = user.email
#         form.phone.data = user.phone
#         form.info.data = user.info
#     if form.validate_on_submit():
#         data = form.data
#         print(form.name)
#         print(form.avatar)
#         print(form.avatar.data)
#         print(type(form.avatar.data))
#         if form.avatar.data:
#             file_avatar = secure_filename(form.avatar.data.filename)
#             if not os.path.exists(current_app.config['UP_DIR']):
#                 os.makedirs(current_app.config['UP_DIR'])
#             user.avatar = change_filename(file_avatar)
#             form.avatar.data.save(current_app.config['UP_DIR'] + user.avatar)
#
#         name_count = User.query.filter_by(name=data['name']).count()
#         if data['name'] != user.name and name_count == 1:
#             flash('昵称已经存在！', 'err')
#             return redirect(url_for('home.user'))
#         email_count = User.query.filter_by(email=data['email']).count()
#         if data['email'] != user.email and email_count == 1:
#             flash('邮箱已经存在！', 'err')
#             return redirect(url_for('home.user'))
#         phone_count = User.query.filter_by(phone=data['phone']).count()
#         if data['phone'] != user.phone and phone_count == 1:
#             flash('手机号码已经存在！', 'err')
#             return redirect(url_for('home.user'))
#         user.name = data['name']
#         user.email = data['email']
#         user.phone = data['phone']
#         user.info = data['info']
#         db.session.add(user)
#         db.session.commit()
#         flash('修改成功！', 'ok')
#         return redirect(url_for('home.user'))
#     return render_template('home/user.html', form=form, user=user)


@home.route('/pwd/', methods=['GET', 'POST'])
@user_login_req
def pwd():
    return render_template('home/pwd.html')


@home.route('/comments/', methods=['GET', 'POST'])
@user_login_req
def comments():
    return render_template('home/comments.html')


@home.route('/loginlog/', methods=['GET', 'POST'])
@user_login_req
def loginlog():
    return render_template('home/loginlog.html')


@home.route('/moviefav/', methods=['GET', 'POST'])
@user_login_req
def moviefav():
    return render_template('home/moviefav.html')


@home.route('/animation/', methods=['GET', 'POST'])
def animation():
    return render_template('home/animation.html')


@home.route('/search/', methods=['GET', 'POST'])
def search():
    return render_template('home/search.html')


@home.route('/play/', methods=['GET', 'POST'])
def play():
    return render_template('home/play.html')
