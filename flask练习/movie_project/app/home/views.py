"""
Created by dreamkong on 2018/10/31
"""
import uuid

from app import bcrypt, db
from app.home.forms import RegisterForm, LoginForm
from app.models import User, UserLog
from . import home
from flask import render_template, redirect, url_for, flash, request, session

__author__ = 'dreamkong'


@home.route('/', methods=['GET'])
def index():
    return render_template('home/index.html')


# @home.route('/login/', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         data = form.data
#         user = User.query.filter_by(name=data['name']).first()
#         if user.check_password(data['password']):
#             flash('密码错误！', 'err')
#             return redirect(url_for('home.login'))
#         session['user'] = user.name
#         session['user_id'] = user.id
#         user_log = UserLog(
#             user_id=user.id,
#             ip=request.remote_addr
#         )
#         db.session.add(user_log)
#         db.session.commit()
#         return redirect(url_for('home.user'))
#     return render_template('home/login.html', form=form)


@home.route('/logout/', methods=['GET'])
def logout():
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


@home.route('/user/', methods=['GET'])
def user():
    return render_template('home/user.html')


@home.route('/pwd/', methods=['GET', 'POST'])
def pwd():
    return render_template('home/pwd.html')


@home.route('/comments/', methods=['GET', 'POST'])
def comments():
    return render_template('home/comments.html')


@home.route('/loginlog/', methods=['GET', 'POST'])
def loginlog():
    return render_template('home/loginlog.html')


@home.route('/moviefav/', methods=['GET', 'POST'])
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
