"""
Created by dreamkong on 2018/10/31
"""
from flask import Flask, render_template
from flask_bcrypt import Bcrypt

from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint
from app.models import db

__author__ = 'dreamkong'

bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(home_blueprint)

    # 注册flask_sqlalchemy
    db.init_app(app)
    db.create_all(app=app)

    bcrypt.init_app(app)

    # 404
    @app.errorhandler(404)
    def page_not_find(error):
        return render_template('home/404.html'), 404

    return app
