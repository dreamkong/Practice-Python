"""
Created by dreamkong on 2018/10/31
"""
import uuid
from datetime import datetime
from functools import wraps

import os
from werkzeug.utils import secure_filename

from app import bcrypt
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm, PasswordForm, AuthForm, RoleForm, AdminForm
from app.models import Admin, Tag, db, Movie, Preview, User, Comment, MovieFav, OperateLog, AdminLog, UserLog, Auth, \
    Role
from manage import app

__author__ = 'dreamkong'

from . import admin
from flask import render_template, redirect, url_for, flash, session, request, abort


@app.context_processor
def tpl_extra():
    data = dict(
        online_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    return data


# 权限控制装饰器
def admin_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = Admin \
            .query \
            .join(Role) \
            .filter(Admin.role_id == Role.id, Admin.id == session['admin_id']) \
            .first()
        auths = admin.role.auths
        if auths:
            auths = list(map(lambda v: int(v), auths.split(',')))
        else:
            auths = []
        auth_list = Auth.query.all()
        urls = [v.url for v in auth_list for val in auths if v == val]
        rule = request.url_rule
        if str(rule) not in urls:
            abort(404)
        return f(*args, **kwargs)

    return decorated_function


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


# 添加operate_log
def add_operate_log(reason):
    operate_log = OperateLog(
        admin_id=session['admin_id'],
        ip=request.remote_addr,
        reason=reason
    )
    db.session.add(operate_log)
    db.session.commit()


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
        session['admin_id'] = admin.id
        admin_log = AdminLog(
            admin_id=admin.id,
            ip=request.remote_addr
        )
        db.session.add(admin_log)
        db.session.commit()
        return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/login.html', form=form)


@admin.route('/logout/')
@admin_login_req
def logout():
    session.pop('admin', None)
    session.pop('admin_id', None)
    return redirect(url_for('admin.login'))


@admin.route('/pwd/', methods=['GET', 'POST'])
@admin_login_req
def pwd():
    form = PasswordForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=session['admin']).first()
        admin.password = bcrypt.generate_password_hash(data['new_password'])
        db.session.add(admin)
        db.session.commit()
        flash('修改密码成功，请重新登录！', 'ok')
        reason = '修改密码'
        add_operate_log(reason)
        return redirect(url_for('admin.logout'))
    return render_template('admin/pwd.html', form=form)


@admin.route('/tag/list/<int:page>', methods=['GET'])
@admin_login_req
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(Tag.add_time.desc()).paginate(page=page, per_page=app.config['PER_PAGE'])
    return render_template('admin/tag_list.html', page_data=page_data)


@admin.route('/tag/add', methods=['GET', 'POST'])
@admin_auth
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
        reason = '添加了一个标签：{}'.format(tag.name)
        add_operate_log(reason)
        return redirect(url_for('admin.tag_list', page=1))
    return render_template('admin/tag_add.html', form=form)


@admin.route('/tag/delete/<int:id>/', methods=['GET'])
@admin_auth
@admin_login_req
def tag_delete(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('删除成功', 'ok')
    reason = '删除了一个标签：{}'.format(tag.name)
    add_operate_log(reason)
    return redirect(url_for('admin.tag_list', page=1))


@admin.route('/tag/edit/<int:id>', methods=['GET', 'POST'])
@admin_auth
@admin_login_req
def tag_edit(id=None):
    tag = Tag.query.get_or_404(id)
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        old_tag_name = tag.name
        if tag.name != data['name'] and tag_count == 1:
            flash('名称已经存在！', 'err')
            return redirect(url_for('admin.tag_edit', id=id))
        tag.name = data['name']
        db.session.add(tag)
        db.session.commit()
        flash('修改标签成功！', 'ok')
        reason = '修改了一个标签：{}->{}'.format(old_tag_name, tag.name)
        add_operate_log(reason)
        return redirect(url_for('admin.tag_list', page=1))
    return render_template('admin/tag_edit.html', form=form, tag=tag)


@admin.route('/movie/list/<int:page>', methods=['GET'])
@admin_login_req
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.order_by(Movie.add_time.desc()).paginate(page=page, per_page=app.config['PER_PAGE'])
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
        reason = '添加了一个电影：{}'.format(movie.name)
        add_operate_log(reason)
        return redirect(url_for('admin.movie_list', page=1))
    return render_template('admin/movie_add.html', form=form)


@admin.route('/movie/delete/<int:id>', methods=['GET'])
@admin_login_req
def movie_delete(id=None):
    movie = Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    flash('删除电影成功！', 'ok')
    reason = '删除了一个电影：{}'.format(movie.name)
    add_operate_log(reason)
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
        reason = '修改了一个电影：{}'.format(movie.name)
        add_operate_log(reason)
        return redirect(url_for('admin.movie_list', page=1))
    return render_template('admin/movie_edit.html', form=form, movie=movie)


@admin.route('/preview/list/<int:page>', methods=['GET'])
@admin_login_req
def preview_list(page=None):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(Preview.add_time.desc()).paginate(per_page=app.config['PER_PAGE'], page=page)
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
        reason = '添加了一个预告：{}'.format(preview.name)
        add_operate_log(reason)
        return redirect(url_for('admin.preview_list', page=1))
    return render_template('admin/preview_add.html', form=form)


@admin.route('/preview/delete/<int:id>', methods=['GET'])
@admin_login_req
def preview_delete(id=None):
    preview = Preview.query.get_or_404(int(id))
    db.session.delete(preview)
    db.session.commit()
    flash('删除预告成功！', 'ok')
    reason = '删除了一个预告：{}'.format(preview.name)
    add_operate_log(reason)
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
        reason = '修改了一个预告：{}'.format(preview.name)
        add_operate_log(reason)
        return redirect(url_for('admin.preview_list', page=1))
    return render_template('admin/preview_edit.html', form=form, preview=preview)


@admin.route('/user/list/<int:page>', methods=['GET'])
@admin_login_req
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(User.id.desc()).paginate(page=page, per_page=app.config['PER_PAGE'])
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
    reason = '删除了一个用户：{}'.format(user.name)
    add_operate_log(reason)
    return redirect(url_for('admin.user_list', page=1))


@admin.route('/comment/list/<int:page>', methods=['GET'])
@admin_login_req
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query \
        .join(Movie) \
        .join(User) \
        .filter(Movie.id == Comment.movie_id, User.id == Comment.user_id) \
        .order_by(Comment.add_time.desc()) \
        .paginate(page=page, per_page=app.config['PER_PAGE'])
    return render_template('admin/comment_list.html', page_data=page_data)


@admin.route('/comment/delete/<int:id>', methods=['GET'])
@admin_login_req
def comment_delete(id=None):
    comment = Comment.query.get_or_404(int(id))
    db.session.delete(comment)
    db.session.commit()
    flash('删除评论成功！', 'ok')
    reason = '删除了一个评论：{}'.format(comment.name)
    add_operate_log(reason)
    return redirect(url_for('admin.comment_list', page=1))


@admin.route('/movie_fav/list/<int:page>', methods=['GET'])
@admin_login_req
def movie_fav_list(page=None):
    if page is None:
        page = 1
    page_data = MovieFav.query \
        .join(Movie) \
        .join(User) \
        .filter(Movie.id == MovieFav.movie_id, User.id == MovieFav.user_id) \
        .order_by(MovieFav.add_time.desc()) \
        .paginate(page=page, per_page=app.config['PER_PAGE'])
    return render_template('admin/movie_fav_list.html', page_data=page_data)


@admin.route('/movie_fav/delete/<int:id>', methods=['GET'])
@admin_login_req
def movie_fav_delete(id=None):
    movie_fav = MovieFav.query.join(Movie).filter(MovieFav.movie_id == Movie.id).get_or_404(int(id))
    db.session.delete(movie_fav)
    db.session.commit()
    flash('删除电影收藏成功！', 'ok')
    reason = '删除了一个电影收藏：{}'.format(movie_fav.movie.name)
    add_operate_log(reason)
    return redirect(url_for('admin.movie_fav_list', page=1))


@admin.route('/operate_log/list/<int:page>', methods=['GET'])
@admin_login_req
def operate_log_list(page=None):
    if page is None:
        page = 1
    page_data = OperateLog \
        .query \
        .join(Admin) \
        .filter(OperateLog.admin_id == Admin.id) \
        .order_by(OperateLog.add_time.desc()) \
        .paginate(page=page, per_page=app.config['PER_PAGE'])
    return render_template('admin/operate_log_list.html', page_data=page_data)


@admin.route('/admin_log/list/<int:page>', methods=['GET'])
@admin_login_req
def admin_log_list(page):
    if page is None:
        page = 1
    page_data = AdminLog \
        .query \
        .join(Admin) \
        .filter(AdminLog.admin_id == Admin.id) \
        .order_by(AdminLog.add_time.desc()) \
        .paginate(page=page, per_page=app.config['PER_PAGE'])
    return render_template('admin/admin_log_list.html', page_data=page_data)


@admin.route('/user_log/list/<int:page>', methods=['GET'])
@admin_login_req
def user_log_list(page):
    if page is None:
        page = 1
    page_data = UserLog \
        .query \
        .join(User) \
        .filter(UserLog.user_id == User.id) \
        .order_by(UserLog.add_time.desc()) \
        .paginate(page=page, per_page=app.config['PER_PAGE'])
    return render_template('admin/user_log_list.html', page_data=page_data)


@admin.route('/auth/list/<int:page>', methods=['GET'])
@admin_login_req
def auth_list(page):
    if page is None:
        page = 1
    page_data = Auth.query.order_by(Auth.add_time.desc()).paginate(per_page=app.config['PER_PAGE'], page=page)
    return render_template('admin/auth_list.html', page_data=page_data)


@admin.route('/auth/add', methods=['GET', 'POST'])
@admin_login_req
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(
            name=data['name'],
            url=data['url']
        )
        db.session.add(auth)
        db.session.commit()
        flash('权限添加成功', 'ok')
        reason = '添加了一个权限：{}'.format(auth.name)
        add_operate_log(reason)
        return redirect(url_for('admin.auth_list', page=1))
    return render_template('admin/auth_add.html', form=form)


@admin.route('/auth/delete/<int:id>/', methods=['GET'])
@admin_login_req
def auth_delete(id=None):
    auth = Auth.query.filter_by(id=id).first_or_404()
    db.session.delete(auth)
    db.session.commit()
    flash('删除成功', 'ok')
    reason = '删除了一个权限：{}'.format(auth.name)
    add_operate_log(reason)
    return redirect(url_for('admin.auth_list', page=1))


@admin.route('/auth/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_req
def auth_edit(id=None):
    auth = Auth.query.get_or_404(id)
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth_count = Auth.query.filter_by(name=data['name']).count()
        old_auth_name = auth.name
        if auth.name != data['name'] and auth_count == 1:
            flash('名称已经存在！', 'err')
            return redirect(url_for('admin.auth_edit', id=id))
        auth.name = data['name']
        auth.url = data['url']
        db.session.add(auth)
        db.session.commit()
        flash('修改权限成功！', 'ok')
        reason = '修改了一个权限：{}->{}'.format(old_auth_name, auth.name)
        add_operate_log(reason)
        return redirect(url_for('admin.auth_list', page=1))
    return render_template('admin/auth_edit.html', form=form, auth=auth)


@admin.route('/role/list/<int:page>', methods=['GET'])
@admin_login_req
def role_list(page):
    if page is None:
        page = 1
    page_data = Role.query.order_by(Role.add_time.desc()).paginate(per_page=app.config['PER_PAGE'], page=page)
    return render_template('admin/role_list.html', page_data=page_data)


@admin.route('/role/add', methods=['GET', 'POST'])
@admin_login_req
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        role = Role(
            name=data['name'],
            auths=','.join(map(lambda v: str(v), data['auths']))
        )
        db.session.add(role)
        db.session.commit()
        flash('添加角色成功', 'ok')
        return redirect(url_for('admin.role_list', page=1))
    return render_template('admin/role_add.html', form=form)


@admin.route('/role/delete/<int:id>/', methods=['GET'])
@admin_login_req
def role_delete(id=None):
    role = Role.query.filter_by(id=id).first_or_404()
    db.session.delete(role)
    db.session.commit()
    flash('删除成功', 'ok')
    reason = '删除了一个权限：{}'.format(role.name)
    add_operate_log(reason)
    return redirect(url_for('admin.role_list', page=1))


@admin.route('/role/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_req
def role_edit(id):
    role = Role.query.get_or_404(id)
    form = RoleForm()
    if request.method == 'GET':
        form.auths.data = list(map(lambda v: int(v), role.auths.split(',')))
    if form.validate_on_submit():
        data = form.data
        role.name = data['name']
        role.auths = ','.join(map(lambda v: str(v), data['auths']))
        db.session.add(role)
        db.session.commit()
        flash('修改标签成功！', 'ok')
        return redirect(url_for('admin.role_list', page=1))
    return render_template('admin/role_edit.html', form=form, role=role)


@admin.route('/admin/list/<int:page>', methods=['GET'])
@admin_login_req
def admin_list(page):
    if page is None:
        page = 1
    page_data = Admin.query.join(Role).filter(Admin.role_id == Role.id).order_by(Admin.add_time.desc()).paginate(
        per_page=app.config['PER_PAGE'], page=page)
    return render_template('admin/admin_list.html', page_data=page_data)


@admin.route('/admin/add', methods=['GET', 'POST'])
@admin_login_req
def admin_add():
    form = AdminForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin(
            name=data['name'],
            password=bcrypt.generate_password_hash(data['password']),
            # is_super=data['is_super'],
            role_id=data['role_id']
        )
        db.session.add(admin)
        db.session.commit()
        flash('添加管理员成功！', 'ok')
        return redirect(url_for('admin.admin_list', page=1))
    return render_template('admin/admin_add.html', form=form)


@admin.route('/admin/delete/<int:id>/', methods=['GET'])
@admin_login_req
def admin_delete(id=None):
    admin = Admin.query.filter_by(id=id).first_or_404()
    db.session.delete(admin)
    db.session.commit()
    flash('删除成功', 'ok')
    reason = '删除了一个管理员：{}'.format(admin.name)
    add_operate_log(reason)
    return redirect(url_for('admin.admin_list', page=1))


@admin.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_req
def admin_edit(id):
    admin = Admin.query.get_or_404(id)
    form = AdminForm()
    if request.method == 'GET':
        form.auths.data = list(map(lambda v: int(v), admin.auths.split(',')))
    if form.validate_on_submit():
        data = form.data
        admin.name = data['name']
        admin.auths = ','.join(map(lambda v: str(v), data['auths']))
        db.session.add(admin)
        db.session.commit()
        flash('修改标签成功！', 'ok')
        return redirect(url_for('admin.admin_list', page=1))
    return render_template('admin/admin_edit.html', form=form, admin=admin)
