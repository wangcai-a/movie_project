from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import datetime


app = Flask(__name__)
app.config["SQLACHEMY_DATABASE_URI"] = "mysql://root:mysql@127.0.0.1/movie"
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


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Interger, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    movies = db.relationship("Movie", backref="tag") # 电影外键关联

    def __repr__(self):
        return "<Tag %r>" % self.name


class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Interger, primary_key=True)   # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)    # 地址
    info = db.Column(db.Text)   # 简介
    logo = db.Column(db.String(255), unique=True)   # 封面
    star = db.Column(db.SmallInterger)  # 星级
    playnum = db.Column(db.BigInterger) # 播放量
    commentnum = db.Column(db.BigInterger)  # 评论量
    tag_id = db.Column(db.Interger, db.ForeignKey('tag.id'))    # 所属标签
    area = db.Column(db.String(255))    # 地区
    release_time = db.Column(db.Date)   # 上映时间
    length = db.Column(db.String)   # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)   # 添加时间

    def __repr__(self):
        return "<Moive %r>" % self.title


class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Interger, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Preview %r>" % self.title