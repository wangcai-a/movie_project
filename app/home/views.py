from . import home
from flask import render_template, redirect, url_for, flash
from app.home.froms import RegistForm
from app.models import User
from werkzeug.security import generate_password_hash
import uuid
from app import db


@home.route("/")
def index():
    return render_template("home/index.html")


@home.route("/animation/")
def animation():
    return render_template("home/animation.html")


# 登陆
@home.route("/login/")
def login():
    return render_template("home/login.html")


# 登出
@home.route("/logout/")
def logout():
    return redirect(url_for("home/logout.html"))


# 注册
@home.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        name = User.query.filter_by(name=data["name"]).count()
        email = User.query.filter_by(email=data["email"]).count()
        if name:
            flash("昵称已经被注册,请重新填写!", "err")
            return redirect(url_for("home.register"))
        if email:
            flash("邮箱已经存在", "err")
            return redirect(url_for("home.register"))
        user = User(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            pwd=generate_password_hash(data["pwd"]),
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功", "ok")
    return render_template("home/register.html", form=form)


# 会员中心
@home.route("/user/")
def user():
    return render_template("home/user.html")


# 修改密码
@home.route("/pwd/")
def pwd():
    return render_template("home/pwd.html")


# 评论
@home.route("/comments/")
def comments():
    return render_template("home/comments.html")


# 登陆日志
@home.route("/loginlog/")
def loginlog():
    return render_template("home/loginlog.html")


@home.route("/moviecol/")
def moviecol():
    return render_template("home/moviecol.html")


# 电影搜索
@home.route("/search/")
def search():
    return render_template("home/search.html")


# 电影播放
@home.route("/play/")
def play():
    return render_template("home/play.html")


