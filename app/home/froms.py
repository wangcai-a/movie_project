from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, regexp, ValidationError
from app.models import User


class RegistForm(FlaskForm):
    name = StringField(
        label="昵称",
        validators=[
            DataRequired("请输入昵称")
        ],
        description="昵称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入昵称",
            "required": "required"
        }
    )

    pwd = PasswordField(
        label="密码",
        validators={
            DataRequired("请输入密码")
        },
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码",
            "required": "required"
        }
    )

    re_pwd = PasswordField(
        label="确认密码",
        validators={
            DataRequired("请输入密码"),
            EqualTo('pwd', message="两次输入不一致")
        },
        description="请确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入确认密码",
            "required": "required"
        }
    )

    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱"),
            Email("邮箱格式不正确")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱",
            "required": "required"
        }
    )

    phone = StringField(
        label="手机号码",
        validators=[
            DataRequired("请输入手机号码"),
            regexp("1[3458]\\d{9}", message="手机格式不正确")
        ],
        description="手机号码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机号码",
            "required": "required"
        }
    )

    submit = SubmitField(
        "注册",
        render_kw={
            "class": "btn btn-lg btn-success btn-block"
        }
    )

    def validata_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError("昵称已经存在!")

    def validata_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError("邮箱已经存在!")

    def validata_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError("手机号码已经存在!")


class LoginForm(FlaskForm):
    """会员登陆表单"""
    name = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号",
            "required": "required"
        }
    )

    pwd = PasswordField(
        label="密码",
        validators={
            DataRequired("请输入密码")
        },
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码",
            "required": "required"
        }
    )

    submit = SubmitField(
        "登陆",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )