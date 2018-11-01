"""
Created by dreamkong on 2018/10/31
"""

__author__ = 'dreamkong'

from . import admin
from flask import render_template, redirect, url_for

@admin.route('/')
def index():
    return render_template('admin/index.html')

@admin.route('/login/')
def login():
    return render_template('admin/login.html')

@admin.route('/logout/')
def logout():
    return redirect(url_for('admin.login'))

@admin.route('/pwd/')
def pwd():
    return render_template('admin/pwd.html')

@admin.route('/tag/list')
def tag_list():
    return render_template('admin/tag_list.html')

@admin.route('/tag/add')
def tag_add():
    return render_template('admin/tag_add.html')

@admin.route('/movie/list')
def movie_list():
    return render_template('admin/movie_list.html')

@admin.route('/movie/add')
def movie_add():
    return render_template('admin/movie_add.html')

@admin.route('/preview/list')
def preview_list():
    return render_template('admin/preview_list.html')

@admin.route('/preview/add')
def preview_add():
    return render_template('admin/preview_add.html')

@admin.route('/user/list')
def user_list():
    return render_template('admin/user_list.html')

@admin.route('/user/view')
def user_view():
    return render_template('admin/user_view.html')

@admin.route('/comment/list')
def comment_list():
    return render_template('admin/comment_list.html')

@admin.route('/movie_fav/list')
def movie_fav_list():
    return render_template('admin/movie_fav_list.html')

@admin.route('/operate_log/list')
def operate_log_list():
    return render_template('admin/operate_log_list.html')

@admin.route('/admin_log/list')
def admin_log_list():
    return render_template('admin/admin_log_list.html')

@admin.route('/user_log/list')
def user_log_list():
    return render_template('admin/user_log_list.html')

@admin.route('/auth/list')
def auth_list():
    return render_template('admin/auth_list.html')

@admin.route('/auth/add')
def auth_add():
    return render_template('admin/auth_add.html')

@admin.route('/role/list')
def role_list():
    return render_template('admin/role_list.html')

@admin.route('/role/add')
def role_add():
    return render_template('admin/role_add.html')

@admin.route('/admin/list')
def admin_list():
    return render_template('admin/admin_list.html')

@admin.route('/admin/add')
def admin_add():
    return render_template('admin/admin_add.html')