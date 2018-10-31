"""
Created by dreamkong on 2018/10/31
"""
from flask import Blueprint

__author__ = 'dreamkong'

home = Blueprint('home', __name__)
from app.home import views
