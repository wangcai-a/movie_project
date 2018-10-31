from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.home.froms import RegistForm, LoginForm
from app.models import User, Userlog
from werkzeug.security import generate_password_hash
import uuid
from app import db
from functools import wraps


# 定义访问控制装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# 主页
@home.route("/")
@user_login_req
def index():
    return render_template("home/index.html")


@home.route("/animation/")
@user_login_req
def animation():
    return render_template("home/animation.html")


# 登陆
@home.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if not user.check_pwd(data["pwd"]):
            flash("密码错误", "err")
            return redirect(url_for("home.login"))
        session["user"] = user.name
        session["user"] = user.id
        userlog = Userlog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.user"))
    return render_template("home/login.html", form=form)


# 登出
@home.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for("home.login"))


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
@user_login_req
def user():
    return render_template("home/user.html")


# 修改密码
@home.route("/pwd/")
@user_login_req
def pwd():
    return render_template("home/pwd.html")


# 评论
@home.route("/comments/")
@user_login_req
def comments():
    return render_template("home/comments.html")


# 登陆日志
@home.route("/loginlog/")
@user_login_req
def loginlog():
    return render_template("home/loginlog.html")


@home.route("/moviecol/")
@user_login_req
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


