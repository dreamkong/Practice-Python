"""
Created by dreamkong on 2018/10/31
"""
import uuid
from datetime import datetime
from functools import wraps

import os
from werkzeug.utils import secure_filename

from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm
from app.models import Admin, Tag, db, Movie, Preview, User, Comment
from manage import app

__author__ = 'dreamkong'

from . import admin
from flask import render_template, redirect, url_for, flash, session, request


# 登录装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@admin.route('/')
@admin_login_req
def index():
    return render_template('admin/index.html')


@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if not admin.check_password(data['password']):
            flash('密码错误！')
            return redirect(url_for('admin.login'))
        session['admin'] = data['account']
        return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/login.html', form=form)


@admin.route('/logout/')
@admin_login_req
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


@admin.route('/pwd/')
@admin_login_req
def pwd():
    return render_template('admin/pwd.html')


@admin.route('/tag/list/<int:page>', methods=['GET'])
@admin_login_req
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(Tag.add_time.desc()).paginate(page=page, per_page=10)
    return render_template('admin/tag_list.html', page_data=page_data)


@admin.route('/tag/add', methods=['GET', 'POST'])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data['name']).count()
        if tag == 1:
            flash('名称已经存在！', 'err')
            return redirect(url_for('admin.tag_add'))
        tag = Tag(
            name=data['name']
        )
        db.session.add(tag)
        db.session.commit()
        flash('添加标签成功！', 'ok')
        return redirect(url_for('admin.tag_list', page=1))
    return render_template('admin/tag_add.html', form=form)


@admin.route('/tag/delete/<int:id>/', methods=['GET'])
@admin_login_req
def tag_delete(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('删除成功', 'ok')
    return redirect(url_for('admin.tag_list', page=1))


@admin.route('/tag/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_req
def tag_edit(id=None):
    tag = Tag.query.get_or_404(id)
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        print(type(data))
        print(data)
        if tag.name != data['name'] and tag_count == 1:
            flash('名称已经存在！', 'err')
            return redirect(url_for('admin.tag_edit', id=id))
        tag.name = data['name']
        db.session.add(tag)
        db.session.commit()
        flash('修改标签成功！', 'ok')
        return redirect(url_for('admin.tag_list', page=1))
    return render_template('admin/tag_edit.html', form=form, tag=tag)


@admin.route('/movie/list/<int:page>', methods=['GET'])
@admin_login_req
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.order_by(Movie.add_time.desc()).paginate(page=page, per_page=10)
    return render_template('admin/movie_list.html', page_data=page_data)


@admin.route('/movie/add', methods=['GET', 'POST'])
@admin_login_req
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config['UP_DIR'] + url)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            play_nums=0,
            comment_nums=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length']
        )
        db.session.add(movie)
        db.session.commit()
        flash('添加电影成功！', 'ok')
        return redirect(url_for('admin.movie_list', page=1))
    return render_template('admin/movie_add.html', form=form)


@admin.route('/movie/delete/<int:id>', methods=['GET'])
@admin_login_req
def movie_delete(id=None):
    movie = Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    flash('删除电影成功！', 'ok')
    return redirect(url_for('admin.movie_list', page=1))


@admin.route('/movie/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_req
def movie_edit(id=None):
    movie = Movie.query.get_or_404(int(id))
    form = MovieForm()
    if request.method == 'GET':
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star

    # 因为是编辑，所以非空验证空
    form.url.validators = []
    form.logo.validators = []
    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title=data['title']).count()
        if movie.title != data['title'] and movie_count == 1:
            flash('片名已经存在！', 'err')
            return redirect(url_for('admin.movie_edit', id=id))

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')

        if form.url.data:
            file_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)
            form.url.data.save(app.config['UP_DIR'] + movie.url)

        if form.logo.data:
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + movie.logo)

        movie.title = data['title'],
        movie.info = data['info'],
        movie.star = int(data['star']),
        movie.tag_id = int(data['tag_id']),
        movie.area = data['area'],
        movie.release_time = data['release_time'],
        movie.length = data['length']
        db.session.add(movie)
        db.session.commit()
        flash('修改电影成功！')
        return redirect(url_for('admin.movie_list', page=1))
    return render_template('admin/movie_edit.html', form=form, movie=movie)


@admin.route('/preview/list/<int:page>', methods=['GET'])
@admin_login_req
def preview_list(page=None):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(Preview.add_time.desc()).paginate(per_page=10, page=page)
    return render_template('admin/preview_list.html', page_data=page_data)


@admin.route('/preview/add', methods=['GET', 'POST'])
@admin_login_req
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')

        file_logo = secure_filename(form.logo.data.filename)
        logo = change_filename(file_logo)
        form.logo.data.save(app.config['UP_DIR'] + logo)

        preview = Preview(
            title=data['title'],
            logo=logo
        )
        db.session.add(preview)
        db.session.commit()
        flash('添加预告成功！', 'ok')
        return redirect(url_for('admin.preview_list', page=1))
    return render_template('admin/preview_add.html', form=form)


@admin.route('/preview/delete/<int:id>', methods=['GET'])
@admin_login_req
def preview_delete(id=None):
    preview = Preview.query.get_or_404(int(id))
    db.session.delete(preview)
    db.session.commit()
    flash('删除预告成功！', 'ok')
    return redirect(url_for('admin.preview_list', page=1))


@admin.route('/preview/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_req
def preview_edit(id=None):
    preview = Preview.query.get_or_404(int(id))
    form = PreviewForm()
    form.logo.validators = []
    if form.validate_on_submit():
        data = form.data
        preview_count = Preview.query.filter_by(title=data['title']).count()
        if data['title'] != preview.title and preview_count == 1:
            flash('预告已经存在！', 'err')
            return redirect(url_for('admin.preview_edit', id=id))

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR', 'rw'])

        if form.logo.data:
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + preview.logo)

        preview.title = data['title']
        db.session.add(preview)
        db.session.commit()
        flash('修改预告成功！', 'ok')
        return redirect(url_for('admin.preview_list', page=1))
    return render_template('admin/preview_edit.html', form=form, preview=preview)


@admin.route('/user/list/<int:page>', methods=['GET'])
@admin_login_req
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(User.id.desc()).paginate(page=page, per_page=10)
    return render_template('admin/user_list.html', page_data=page_data)


@admin.route('/user/view/<int:id>', methods=['GET'])
@admin_login_req
def user_view(id=None):
    user = User.query.get_or_404(id)
    return render_template('admin/user_view.html', user=user)


@admin.route('/user/delete/<int:id>', methods=['GET'])
@admin_login_req
def user_delete(id=None):
    user = User.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    flash('删除用户成功！', 'ok')
    return redirect(url_for('admin.user_list', page=1))


@admin.route('/comment/list/<int:page>', methods=['GET'])
@admin_login_req
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query\
        .join(Movie)\
        .join(User)\
        .filter(Movie.id == Comment.movie_id,User.id == Comment.user_id)\
        .order_by(Comment.add_time.desc())\
        .paginate(page=page, per_page=10)
    return render_template('admin/comment_list.html', page_data=page_data)


@admin.route('/movie_fav/list', methods=['GET'])
@admin_login_req
def movie_fav_list():
    return render_template('admin/movie_fav_list.html')


@admin.route('/operate_log/list', methods=['GET'])
@admin_login_req
def operate_log_list():
    return render_template('admin/operate_log_list.html')


@admin.route('/admin_log/list', methods=['GET'])
@admin_login_req
def admin_log_list():
    return render_template('admin/admin_log_list.html')


@admin.route('/user_log/list', methods=['GET'])
@admin_login_req
def user_log_list():
    return render_template('admin/user_log_list.html')


@admin.route('/auth/list', methods=['GET'])
@admin_login_req
def auth_list():
    return render_template('admin/auth_list.html')


@admin.route('/auth/add', methods=['GET', 'POST'])
@admin_login_req
def auth_add():
    return render_template('admin/auth_add.html')


@admin.route('/role/list', methods=['GET'])
@admin_login_req
def role_list():
    return render_template('admin/role_list.html')


@admin.route('/role/add', methods=['GET', 'POST'])
@admin_login_req
def role_add():
    return render_template('admin/role_add.html')


@admin.route('/admin/list', methods=['GET'])
@admin_login_req
def admin_list():
    return render_template('admin/admin_list.html')


@admin.route('/admin/add', methods=['GET', 'POST'])
@admin_login_req
def admin_add():
    return render_template('admin/admin_add.html')
