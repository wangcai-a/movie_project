from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.home.froms import RegistForm, LoginForm, UserdetailForm, PwdForm, CommentFrom
from app.models import User, Userlog, Comment, Movie, Moviecol, Tag, Preview
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import uuid
from app import db, app
from functools import wraps
import os
import datetime
import stat


# 定义访问控制装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


# 主页
@home.route("/<int:page>")
@user_login_req
def index(page=None):
    if page is None:
        page = 1
    page_data = Movie.query
    tags = Tag.query.all()
    # 标签
    tid = request.args.get('tid', 0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))
    # 星级
    star = request.args.get('star', 0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))
    # 时间
    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.addtime.asc()
            )
    # 播放量
    pm = request.args.get('pm', 0)
    if int(pm) != 0:
        if int(pm) == 1:
            page_data = page_data.order_by(
                Movie.playnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.playnum.asc()
            )
    # 评论量
    cm = request.args.get('cm', 0)
    if int(cm) != 0:
        if int(cm) == 1:
            page_data = page_data.order_by(
                Movie.commentnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.commentnum.asc()
            )
    page_data = page_data.paginate(page=page, per_page=10)
    p = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm
    )

    # page_data = Movie.query.order_by(
    #     Movie.addtime.desc()
    # ).paginate(page=page, per_page=10)
    return render_template("home/index.html", page_data=page_data, tags=tags, p=p)


# 电影预告
@home.route("/animation/")
@user_login_req
def animation():
    data = Preview.query.all()
    return render_template("home/animation.html", data=data)


# 登陆
@home.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if user:
            if not user.check_pwd(data["pwd"]):
                flash("密码错误", "err")
                return redirect(url_for("home.login"))
            session["user"] = user.name
            session["user_id"] = user.id
            userlog = Userlog(
                user_id=user.id,
                ip=request.remote_addr
            )
            db.session.add(userlog)
            db.session.commit()
            flash('登录成功', 'ok')
            return redirect(url_for("home.user"))
        else:
            flash("账号不存在", 'err')
            return redirect(url_for("home.login"))
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


# 会员中心(修改会员资料)
@home.route("/user/", methods=['GET', 'POST'])
@user_login_req
def user():
    form = UserdetailForm()
    user = User.query.get(int(session["user_id"]))
    form.face.validators = []
    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        file_face = secure_filename(form.face.data.filename)
        if not os.path.exists(app.config["FC_DIR"]):
            os.makedirs(app.config["FC_DIR"])
            os.chmod(app.config["FC_DIR"], stat.S_IRWXU)
        user.face = change_filename(file_face)
        form.face.data.save(app.config["FC_DIR"] + user.face)
        name_count = User.query.filter_by(name=data["name"]).count()
        if data["name"] != user.name and name_count == 1:
            flash("昵称已经存在", "err")
            return redirect(url_for('home.user'))
        email_count = User.query.filter_by(email=data["name"]).count()
        if data["email"] != user.email and email_count == 1:
            flash("邮箱已经存在", "err")
            return redirect(url_for('home.user'))
        phone_count = User.query.filter_by(phone=data["phone"]).count()
        if data["phone"] != user.phone and phone_count == 1:
            flash("电话号码已经存在", "err")
            return redirect(url_for('home.user'))
        user.name = data["name"]
        user.name = data["email"]
        user.name = data["phone"]
        user.name = data["info"]
        db.session.add(user)
        db.session.commit()
        flash("修改成功", 'ok')
        return redirect(url_for("home.user"))
    return render_template("home/user.html", form=form, user=user)


# 修改密码
@home.route("/pwd", methods=["GET", "POST"])
@user_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session["user"]).first()
        user.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(user)
        db.session.commit()
        flash("密码修改成功, 请重新登录", 'ok')
        session.pop("user", None)
        session.pop("user_id", None)
        return redirect(url_for("home.login"))
    return render_template("home/pwd.html", form=form)


# 评论记录
@home.route("/comments/<int:page>", methods=["GET"])
@user_login_req
def comments(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(User).filter(
        User.id == session["user_id"]
    ).join(Movie).filter(
        Movie.id == Comment.movie_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("home/comments.html", page_data=page_data)


# 登陆日志
@home.route("/loginlog/<int:page>", methods=["GET"])
@user_login_req
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.join(User).filter(
        User.id == Userlog.user_id
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("home/loginlog.html", page_data=page_data)


# 电影收藏
@home.route("/moviecol/<int:page>")
@user_login_req
def moviecol(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(User).filter(
        Moviecol.user_id == session["user_id"]
    ).join(Movie).filter(
        Moviecol.movie_id == Movie.id
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("home/moviecol.html", page_data=page_data)


# 电影搜索
@home.route("/search/<int:page>")
def search(page=None):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    movie_count = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')
    ).count()
    page_data = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("home/search.html", page_data=page_data, key=key, movie_count=movie_count)


# 电影播放页面
@home.route("/play/<int:id>/<int:page>", methods=["GET", "POST"])
def play(id=None, page=None):
    if page is None:
        page = 1
    movie = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id,
        Movie.id == int(id)
    ).first_or_404()
    movie.playnum = movie.playnum + 1
    form = CommentFrom()
    if "user" in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data["content"],
            movie_id=movie.id,
            user_id=session["user_id"]
        )
        db.session.add(comment)
        db.session.commit()
        movie.commentnum = movie.commentnum + 1
        db.session.add(movie)
        db.session.commit()
        flash("添加评论成功", "ok")
        return redirect(url_for('home.play', id=movie.id, page=1))
    db.session.add(movie)
    db.session.commit()
    page_data = Comment.query.join(Movie).filter(
        Comment.movie_id == Movie.id,
        Movie.id == int(id)
    ).join(User).filter(
        User.id == Comment.user_id
    ).paginate(page=page, per_page=10)
    return render_template("home/play.html", page_data=page_data, movie=movie, form=form)


