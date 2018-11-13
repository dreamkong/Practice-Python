# coding:utf8
"""
Created by dreamkong on 2018/10/31
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError

from app.models import User

__author__ = 'dreamkong'


class RegisterForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            DataRequired('请输入昵称！')
        ],
        description='昵称',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入昵称！',
            'required': False
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱！'),
            Email('邮箱格式不正确！')
        ],
        description='邮箱',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入邮箱！',
            'required': False
        }
    )
    phone = StringField(
        label='手机号码',
        validators=[
            DataRequired('请输入手机号码！'),
            Regexp('1[345789]\d{9}', message='手机号码格式不正确！')
        ],
        description='手机号码',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入手机号码！',
            'required': False
        }
    )
    password = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码！')
        ],
        description='密码',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入密码！',
            'required': False
        }
    )
    repassword = PasswordField(
        label='确认密码',
        validators=[
            DataRequired('请确认密码！'),
            EqualTo('password', '两次密码不一致')
        ],
        description='确认密码',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请确认密码！',
            'required': False
        }
    )
    submit = SubmitField(
        label='注册',
        render_kw={
            'class': 'btn btn-lg btn-success btn-block'
        }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError('昵称已经存在！')

    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError('邮箱已经存在！')

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError('电话号码已经存在！')


class LoginForm(FlaskForm):
    name = StringField(
        label='账号',
        validators=[
            DataRequired('请输入账号！')
        ],
        description='账号',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入账号！',
            'required': False
        }
    )
    password = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码！')
        ],
        description='密码',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入密码！',
            'required': False
        }
    )
    submit = SubmitField(
        label='登录',
        render_kw={
            'class': 'btn btn-lg btn-success btn-block'
        }
    )
