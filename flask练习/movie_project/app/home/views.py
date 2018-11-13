"""
Created by dreamkong on 2018/10/31
"""
import uuid
from datetime import datetime
from functools import wraps

import os
from werkzeug.utils import secure_filename

from app import bcrypt, db
from app.home.forms import RegisterForm, LoginForm, UserDetailForm, PasswordForm, CommentForm
from app.models import User, UserLog, Preview, Tag, Movie, Comment

# from manage import app

__author__ = 'dreamkong'

from . import home
from flask import render_template, redirect, url_for, flash, request, session, current_app


def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


# 登录装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@home.route('/<int:page>', methods=['GET'])
def index(page):
    tags = Tag.query.all()
    page_data = Movie.query
    # 标签
    tid = request.args.get('tid', 0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))
    # 星级
    star = request.args.get('star', 0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))
    # 时间
    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(Movie.add_time.desc())
        else:
            page_data = page_data.order_by(Movie.add_time.asc())
    # 播放量
    pm = request.args.get('pm', 0)
    if int(pm) != 0:
        if int(pm) == 1:
            page_data = page_data.order_by(
                Movie.play_nums.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.play_nums.asc()
            )
    # 评论量
    cm = request.args.get('cm', 0)
    if int(cm) != 0:
        if int(cm) == 1:
            page_data = page_data.order_by(
                Movie.comment_nums.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.comment_nums.asc()
            )
    if page is None:
        page = 1
    page_data = page_data.paginate(page=page, per_page=8)
    p = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm,
    )
    return render_template('home/index.html', tags=tags, p=p, page_data=page_data)


@home.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if not user.check_password(data['password']):
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


@home.route('/user/', methods=['GET', 'POST'])
@user_login_req
def user():
    form = UserDetailForm()
    user = User.query.get(int(session['user_id']))
    form.avatar.validators = []
    if request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        print(form.name)
        print(form.avatar)
        print(form.avatar.data)
        print(type(form.avatar.data))
        if form.avatar.data:
            file_avatar = secure_filename(form.avatar.data.filename)
            if not os.path.exists(current_app.config['UP_DIR']):
                os.makedirs(current_app.config['UP_DIR'])
            user.avatar = change_filename(file_avatar)
            form.avatar.data.save(current_app.config['UP_DIR'] + user.avatar)

        name_count = User.query.filter_by(name=data['name']).count()
        if data['name'] != user.name and name_count == 1:
            flash('昵称已经存在！', 'err')
            return redirect(url_for('home.user'))
        email_count = User.query.filter_by(email=data['email']).count()
        if data['email'] != user.email and email_count == 1:
            flash('邮箱已经存在！', 'err')
            return redirect(url_for('home.user'))
        phone_count = User.query.filter_by(phone=data['phone']).count()
        if data['phone'] != user.phone and phone_count == 1:
            flash('手机号码已经存在！', 'err')
            return redirect(url_for('home.user'))
        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']
        db.session.add(user)
        db.session.commit()
        flash('修改成功！', 'ok')
        return redirect(url_for('home.user'))
    return render_template('home/user.html', form=form, user=user)


@home.route('/pwd/', methods=['GET', 'POST'])
@user_login_req
def pwd():
    form = PasswordForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session['user']).first()
        user.password = bcrypt.generate_password_hash(data['new_password'])
        db.session.add(user)
        db.session.commit()
        flash('修改密码成功，请重新登录！', 'ok')
        return redirect(url_for('home.logout'))
    return render_template('home/pwd.html', form=form)


@home.route('/comments/<int:page>', methods=['GET', 'POST'])
@user_login_req
def comments(page):
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).filter(Comment.movie_id == Movie.id,
                                                 Comment.user_id == session['user_id']).order_by(
        Comment.add_time.desc()).paginate(per_page=current_app.config['PER_PAGE'], page=page)
    return render_template('home/comments.html', page_data=page_data)


@home.route('/loginlog/<int:page>', methods=['GET', 'POST'])
@user_login_req
def loginlog(page):
    if page is None:
        page = 1
    page_data = UserLog.query.filter_by(user_id=int(session['user_id'])).order_by(
        UserLog.add_time.desc()).paginate(per_page=current_app.config['PER_PAGE'],
                                          page=page)
    return render_template('home/loginlog.html', page_data=page_data)


@home.route('/moviefav/<int:page>', methods=['GET', 'POST'])
@user_login_req
def moviefav(page):
    if page is None:
        page = 1
    return render_template('home/moviefav.html')


@home.route('/animation/', methods=['GET', 'POST'])
def animation():
    data = Preview.query.all()
    return render_template('home/animation.html', data=data)


@home.route('/search/<int:page>', methods=['GET', 'POST'])
def search(page):
    if page is None:
        page = 1
    key = request.args.get('key', "")
    movie_count = Movie.query.filter(Movie.title.ilike('%' + key + '%')).order_by(
        Movie.add_time.desc()).count()
    page_data = Movie.query.filter(Movie.title.ilike('%' + key + '%')).order_by(Movie.add_time.desc()).paginate(
        per_page=10, page=page)
    return render_template('home/search.html', page_data=page_data, movie_count=movie_count, key=key)


@home.route('/play/<int:id>/<int:page>', methods=['GET', 'POST'])
def play(id, page):
    movie = Movie.query.join(Tag).filter(Movie.tag_id == Tag.id, Movie.id == int(id)).first_or_404()
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(Comment.movie_id == Movie.id,
                                                            Comment.user_id == User.id).order_by(
        Comment.add_time.desc()).paginate(per_page=current_app.config['PER_PAGE'], page=page)
    movie.play_nums = movie.play_nums + 1
    db.session.add(movie)
    db.session.commit()
    form = CommentForm()
    if form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data['content'],
            user_id=session['user_id'],
            movie_id=movie.id
        )
        db.session.add(comment)
        movie.comment_nums = movie.comment_nums + 1
        db.session.add(movie)
        db.session.commit()
        flash('添加评论成功！', 'ok')
        return redirect(url_for('home.play', id=movie.id, page=1))
    return render_template('home/play.html', movie=movie, form=form, page_data=page_data)
