"""
Created by dreamkong on 2018/10/31
"""
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError

from app.models import Admin, Tag
from manage import app

__author__ = 'dreamkong'

with app.app_context():
    tags = Tag.query.all()
    print('啦啦啦啦', [(v.id, v.name) for v in tags])


class LoginForm(FlaskForm):
    '''
    管理员登录表单
    '''
    account = StringField(
        label='账号',
        validators=[
            DataRequired('请输入账号！')
        ],
        description='账号',
        render_kw={
            'class': 'form-control',
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
            'class': 'form-control',
            'placeholder': '请输入密码！',
            'required': False
        }
    )
    submit = SubmitField(
        label='登录',
        render_kw={
            'class': 'btn btn-primary btn-block btn-flat'
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError('账号不存在')


class TagForm(FlaskForm):
    name = StringField(
        label='名称',
        validators=[
            DataRequired('请输入标签名称！')
        ],
        description='标签',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入标签名称！',
            'required': False
        }
    )
    submit = SubmitField(
        label='编辑',
        render_kw={
            'class': 'btn btn-primary'
        }
    )


class MovieForm(FlaskForm):
    title = StringField(
        label='片名',
        validators=[
            DataRequired('请输入片名！')
        ],
        description='片名',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入片名！',
            'required': False
        }
    )
    url = FileField(
        label='文件',
        validators=[
            DataRequired('请上传文件！')
        ],
        description='文件',
        render_kw={
            'required': False
        }
    )
    info = TextAreaField(
        label='简介',
        validators=[
            DataRequired('请输入简介！')
        ],
        description='简介',
        render_kw={
            'class': 'form-control',
            'rows': '10',
            'required': False
        }
    )
    logo = FileField(
        label='封面',
        validators=[
            DataRequired('请上传封面！')
        ],
        description='封面',
        render_kw={
            'required': False
        }
    )
    star = SelectField(
        label='星级',
        validators=[
            DataRequired('请选择星级！')
        ],
        coerce=int,
        choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')],
        description='星级',
        render_kw={
            'class': 'form-control',
        }
    )
    tag_id = SelectField(
        label='标签',
        validators=[
            DataRequired('请选择标签！')
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in tags],
        description='标签',
        render_kw={
            'class': 'form-control',
        }
    )
    area = StringField(
        label='地区',
        validators=[
            DataRequired('请输入地区！')
        ],
        description='地区',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入地区！',
            'required': False
        }
    )
    length = StringField(
        label='片长',
        validators=[
            DataRequired('请输入片长！')
        ],
        description='片长',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入片长！',
            'required': False
        }
    )
    release_time = StringField(
        label='上映时间',
        validators=[
            DataRequired('请输入上映时间！')
        ],
        description='上映时间',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入上映时间！',
            'required': False
        }
    )
    submit = SubmitField(
        label='确定',
        render_kw={
            'class': 'btn btn-primary'
        }
    )


class PreviewForm(FlaskForm):
    title = StringField(
        label='预告标题',
        validators=[
            DataRequired('请输入预告标题！')
        ],
        description='预告标题',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入预告标题！',
            'required': False
        }
    )
    logo = FileField(
        label='预告封面',
        validators=[
            DataRequired('请上传预告封面！')
        ],
        description='预告封面',
        render_kw={
            'required': False
        }
    )
    submit = SubmitField(
        label='确定',
        render_kw={
            'class': 'btn btn-primary'
        }
    )


class PasswordForm(FlaskForm):
    old_password = PasswordField(
        label='旧密码',
        validators=[
            DataRequired('请输入旧密码！')
        ],
        description='旧密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入旧密码！',
            'required': False
        }
    )
    new_password = PasswordField(
        label='新密码',
        validators=[
            DataRequired('请输入新密码！')
        ],
        description='新密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入新密码！',
            'required': False
        }
    )
    submit = SubmitField(
        label='确定',
        render_kw={
            'class': 'btn btn-primary'
        }
    )

    def validate_old_password(self, field):
        from flask import session
        old_password = field.data
        name = session['admin']
        admin = Admin.query.filter_by(name=name).first()
        if not admin.check_password(old_password):
            raise ValidationError('旧密码不正确！')
