"""
Created by dreamkong on 2018/10/31
"""

__author__ = 'dreamkong'

from . import admin

@admin.route('/')
def index():
    return 'Admin index'