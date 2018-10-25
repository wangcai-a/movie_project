from . import admin
from flask import render_template, url_for, redirect, flash, session, request
from app.admin.froms import LoginForm, TagForm, MovieForm, PreviewForm, AuthForm, RoleForm, PwdForm
from app.models import Admin, Tag, Moviecol, Movie, Preview, User, Comment, Adminlog, Oplog, Userlog, Auth, Role
from functools import wraps
from app import db, app
from werkzeug.utils import secure_filename
import os
import datetime
import uuid
import stat


# 定义访问控制装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


# 主页面
@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html")


# 登录
@admin.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data['pwd']):
            flash("密码错误!", "err")
            return redirect(url_for("admin.login"))
        session["admin"] = data["account"]
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


# 登出
@admin.route("/logout")
@admin_login_req
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))


# 密码修改
@admin.route("/pwd", methods=["GET", "POST"])
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=session["admin"]).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(admin)
        db.session.commit()
        flash("修改密码成功,请重新登录", "ok")
        redirect(url_for('admin.logout'))
    return render_template("admin/pwd.html", form=form)


# 标签添加
@admin.route("/tag/add", methods=['GET', 'POST'])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data['name']).count()
        if tag == 1:
            flash("名称已经存在", "err")
            return redirect(url_for("admin.tag_add"))
        tag = Tag(
            name=data["name"]
        )
        db.session.add(tag)
        db.session.commit()
        flash("添加标签成功", "ok")
        redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form=form)


# 标签列表
@admin.route("/tag/list/<int:page>", methods=["GET"])
@admin_login_req
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)


# 标签删除
@admin.route("/tag/del/<int:id>", methods=["GET"])
@admin_login_req
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash("删除标签成功", "ok")
    return redirect(url_for("admin.tag_list", page=1))


# 标签编辑
@admin.route("/tag/edit/<int:id>", methods=['GET', 'POST'])
@admin_login_req
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag.name != data["name"] and tag_count == 1:
            flash("名称已经存在", "err")
            return redirect(url_for("admin.tag_edit", id=id))
        tag.name = data["name"]
        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功", "ok")
        return redirect(url_for("admin.tag_list", page=1))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


# 电影添加
@admin.route("/movie/add", methods=["GET", "POST"])
@admin_login_req
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], stat.S_IRWXU)
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config["UP_DIR"] + url)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        title = Movie.query.filter_by(title=data['title']).count()
        if title == 1:
            flash("电影已经存在,请重新添加", "err")
            return redirect(url_for("admin.movie_add"))
        movie = Movie(
            title=data["title"],
            url=url,
            info=data["info"],
            logo=logo,
            star=int(data["star"]),
            playnum=0,
            commentnum=0,
            tag_id=data["tag_id"],
            area=data["area"],
            release_time=data["release_time"],
            length=data["length"]
        )
        db.session.add(movie)
        db.session.commit()
        flash("添加电影成功", "ok")
        return redirect(url_for("admin.movie_add"))
    return render_template("admin/movie_add.html", form=form)


# 电影列表
@admin.route("/movie/list/<int:page>", methods=["GET"])
@admin_login_req
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/movie_list.html", page_data=page_data)


# 电影编辑
@admin.route("/movie/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def movie_edit(id=None):
    form = MovieForm()
    movie = Movie.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], stat.S_IRWXU)
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config["UP_DIR"] + url)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        title_count = Movie.query.filter_by(title=data['title']).count()
        if title_count == 1 and movie.title != data["title"]:
            flash("电影已经存在,请重新修改", "err")
            return redirect(url_for("admin.movie_edit", id=id))
        movie = Movie(
            title=data["title"],
            url=url,
            info=data["info"],
            logo=logo,
            star=int(data["star"]),
            playnum=0,
            commentnum=0,
            tag_id=data["tag_id"],
            area=data["area"],
            release_time=data["release_time"],
            length=data["length"]
        )
        db.session.add(movie)
        db.session.commit()
        flash("修改电影成功", "ok")
        return redirect(url_for("admin.movie_list", page=1))
    return render_template("admin/movie_edit.html", form=form)


# 电影删除
@admin.route("/movie/del/<int:id>", methods=["GET"])
@admin_login_req
def movie_del(id=None):
    movie = Movie.query.filter_by(id=id).first_or_404()
    db.session.delete(movie)
    db.session.commit()
    flash("删除电影成功", "ok")
    return redirect(url_for("admin.movie_list", page=1))


# 添加上映预告
@admin.route("/preview/add", methods=["GET", "POST"])
@admin_login_req
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], stat.S_IRWXU)
        logo = change_filename(file_logo)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        title = Preview.query.filter_by(title=data['title']).count()
        if title == 1:
            flash("预告已经存在,请重新添加", "err")
            return redirect(url_for("admin.preview_add"))
        preview = Preview(
            title=data["title"],
            logo=logo
        )
        db.session.add(preview)
        db.session.commit()
        flash("添加标题成功", "ok")
        return redirect(url_for("admin.preview_add"))
    return render_template("admin/preview_add.html", form=form)


# 上映预告列表
@admin.route("/preview/list", methods=["GET"])
@admin_login_req
def preview_list(page=None):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(
        Preview.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/preview_list.html", page_data=page_data)


# 预告编辑
@admin.route("/preview/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def preview_edit(id=None):
    form = PreviewForm()
    preview = Preview.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], stat.S_IRWXU)
        logo = change_filename(file_logo)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        title_count = Preview.query.filter_by(title=data['title']).count()
        if title_count == 1 and preview.title != data["title"]:
            flash("预告已经存在,请重新修改", "err")
            return redirect(url_for("admin.preview_edit", id=id))
        preview = Preview(
            title=data["title"],
            logo=logo
        )
        db.session.add(preview)
        db.session.commit()
        flash("修改预告成功", "ok")
        return redirect(url_for("admin.preview_list", page=1))
    return render_template("admin/preview_edit.html", form=form)


# 预告删除
@admin.route("/preview/del/<int:id>", methods=["GET"])
@admin_login_req
def preview_del(id=None):
    preview = Preview.query.filter_by(id=id).first_or_404()
    db.session.delete(preview)
    db.session.commit()
    flash("删除预告成功", "ok")
    return redirect(url_for("admin.preview_list", page=1))


# 会员列表
@admin.route("/user/list/<int:page>", methods=["GET"])
@admin_login_req
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/user_list.html", page_data=page_data)


# 会员查看
@admin.route("user/view/<int:id>", methods=["GET"])
@admin_login_req
def user_view(id=None):
    user = User.query.get_or_404(int(id))
    return render_template("admin/user_view.html", user=user)


# 会员删除
@admin.route("/user/del/<int:id>", methods=["GET"])
@admin_login_req
def user_del(id=None):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash("会员删除成功", "ok")
    return redirect(url_for("admin.user_list", page=1))


# 评论列表
@admin.route("/cmoment/list/<int:page>", methods=["GET"])
@admin_login_req
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(User).filter(
        User.id == Comment.user_id
    ).join(Movie).filter(
        Movie.id == Comment.movie_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/comment_list.html", page_data=page_data)


# 评论删除
@admin.route("/comment/del/<int:id>", methods=["GET"])
@admin_login_req
def comment_del(id=None):
    comment = Comment.query.filter_by(id=id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    flash("删除评论成功", "ok")
    return redirect(url_for("admin.comment_list", page=1))


# 收藏列表
@admin.route("/moviecol/list/<int:page>", methods=["GET"])
@admin_login_req
def moviecol_list(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(User).filter(
        User.id == Moviecol.user_id
    ).join(Movie).filter(
        Movie.id == Moviecol.movie_id
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/moviecol_list.html", page_data=page_data)


# 操作日志列表
@admin.route("/oplog/list/<int:page>")
@admin_login_req
def oplog_list(page=None):
    if page is None:
        page = 1
    page_data = Oplog.query.join(Admin).filter(
        Admin.id == Oplog.admin_id
    ).order_by(
        Oplog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/oplog_list.html", page_data=page_data)


# 管理员日志列表
@admin.route("/adminloginlog/list/<int:page>")
@admin_login_req
def adminloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Oplog.query.join(Admin).filter(
        Admin.id == Adminlog.admin_id
    ).order_by(
        Oplog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/adminloginlog_list.html", page_data=page_data)


# 会员登录日志列表
@admin.route("/userloginlog/list/<int:page>")
@admin_login_req
def userloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.join(User).filter(
        User.id == Userlog.user_id
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/userloginlog_list.html", page_data=page_data)


# 添加权限
@admin.route("/auth/add", methods=["GET", "POST"])
@admin_login_req
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        name = Auth.query.filter_by(name=data["name"]).count()
        if name == 1:
            flash("权限已存在", "err")
            return redirect(url_for("admin.auth_add"))
        auth = Auth(
            name=data["name"],
            url=data["url"]
        )
        db.session.add(auth)
        db.session.commit()
        flash("权限添加成功", "ok")
        return redirect(url_for("admin.auth_add"))
    return render_template("admin/auth_add.html", form=form)


# 权限列表
@admin.route("/auth/list/<int:page>")
@admin_login_req
def auth_list(page=None):
    if page is None:
        page = 1
    page_data = Auth.query.order_by(
        Auth.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/auth_list.html", page_data=page_data)


# 编辑权限
@admin.route("/auth/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def auth_edit(id=None):
    form = AuthForm()
    auth = Auth.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        name_count = Auth.query.filter_by(name=data["name"]).count()
        if name_count == 1 and auth.name != data["name"]:
            flash("权限已存在,请重新修改", "err")
            return redirect(url_for("admin.auth_add"))
        auth = Auth(
            name=data["name"],
            url=data["url"]
        )
        db.session.add(auth)
        db.session.commit()
        flash("权限修改成功", "ok")
        return redirect(url_for("admin.auth_edit"))
    return render_template("admin/auth_edit.html", form=form)


# 权限删除
@admin.route("/auth/del/<int:id>", methods=["GET"])
@admin_login_req
def auth_del(id=None):
    auth = Auth.query.filter_by(id=id).first_or_404()
    db.session.delete(auth)
    db.session.commit()
    flash("权限删除成功", "ok")
    return redirect(url_for("admin.auth_list", page=1))


# 添加角色
@admin.route("/role/add", methods=["GET", "POST"])
@admin_login_req
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        role = Role(
            name=data["name"],
            auths=",".join(map(lambda v:str(v), data["auths"]))
        )
        db.session.add(role)
        db.session.commit()
        flash("添加角色成功", "ok")
    return render_template("admin/role_add.html", form=form)


# 角色列表
@admin.route("/role/list")
@admin_login_req
def role_list():
    return render_template("admin/role_list.html")


# 添加管理员
@admin.route("/admin/add")
@admin_login_req
def admin_add():
    return render_template("admin/admin_add.html")


# 管理员列表
@admin.route("/admin/list")
@admin_login_req
def admin_list():
    return render_template("admin/admin_list.html")