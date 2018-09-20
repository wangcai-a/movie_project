from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import datetime


app = Flask(__name__)
app.config["SQLACHEMY_DATABASE_URI"] = "mysql://root:mysql@127.0.0.1"
app.config["SQLACHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


# 会员
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)   # 昵称
    pwd = db.Column(db.String(100))     # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), nuique=True)   # 手机号码
    info = db.Column(db.Text)   # 简介
    face = db.Column(db.String(255), unique=True)   # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)   # 创建时间
    uuid = db.Column(db.String(255), unique=True)   # 唯一标识符
    userlogs = db.relationship('Userlog', backref='user')   # 会员日志外键关联

    def __repr__(self):
        return "<User %r>" % self.name


# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Interger, primary_key=True)
    user_id = db.Column(db.Interger, db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<User %r>" % self.id