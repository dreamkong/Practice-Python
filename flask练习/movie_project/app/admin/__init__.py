"""
Created by dreamkong on 2018/10/31
"""

__author__ = 'dreamkong'

from flask import Blueprint

admin = Blueprint('admin', __name__)
from app.admin import views
