"""
Created by dreamkong on 2018/10/31
"""

__author__ = 'dreamkong'

from . import home
from flask import render_template

@home.route('/')
def index():
    return render_template('home/index.html')

@home.route('/login/')
def login():
    return render_template('home/login.html')

@home.route('/logout/')
def logout():
    return render_template('home/login.html')

@home.route('/register/')
def register():
    return render_template('home/register.html')

@home.route('/user/')
def user():
    return render_template('home/user.html')

@home.route('/pwd/')
def pwd():
    return render_template('home/pwd.html')

@home.route('/comments/')
def comments():
    return render_template('home/comments.html')

@home.route('/loginlog/')
def loginlog():
    return render_template('home/loginlog.html')

@home.route('/moviefav/')
def moviefav():
    return render_template('home/moviefav.html')

@home.route('/animation/')
def animation():
    return render_template('home/animation.html')

@home.route('/search/')
def search():
    return render_template('home/search.html')

@home.route('/play/')
def play():
    return render_template('home/play.html')
