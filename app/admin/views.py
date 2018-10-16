from . import admin
from flask import render_template, url_for, redirect
from app.admin.froms import LoginForm

# 主页面
@admin.route("/")
def index():
    return render_template("admin/index.html")


# 登录
@admin.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
    return render_template("admin/login.html", form=form)


# 登出
@admin.route("/logout")
def logout():
    return redirect(url_for("admin.logout"))


# 密码修改
@admin.route("/pwd")
def pwd():
    return render_template("admin/pwd.html")


# 标签添加
@admin.route("/tag/add")
def tag_add():
    return render_template("admin/tag_add.html")


# 标签列表
@admin.route("/tag/list")
def tag_list():
    return render_template("admin/tag_list.html")


# 编辑电影
@admin.route("/movie/add")
def movie_add():
    return render_template("admin/movie_add.html")


# 编辑电影
@admin.route("/movie/list")
def movie_list():
    return render_template("admin/movie_list.html")


# 上映预告
@admin.route("/preview/add")
def preview_add():
    return render_template("admin/preview_add.html")


# 上映预告列表
@admin.route("/preview/list")
def preview_list():
    return render_template("admin/preview_list.html")


# 会员列表
@admin.route("/user/list")
def user_list():
    return render_template("admin/user_list.html")


# 评论列表
@admin.route("/cmoment/list")
def comment_list():
    return render_template("admin/comment_list.html")


# 收藏列表
@admin.route("/moviecol/list")
def moviecol_list():
    return render_template("admin/moviecol_list.html")


# 操作日志列表
@admin.route("/oplog/list")
def oplog_list():
    return render_template("admin/oplog_list.html")


# 管理员日志列表
@admin.route("/adminloginlog/list")
def adminloginlog_list():
    return render_template("admin/adminloginlog_list.html")


# 会员登录日志列表
@admin.route("/userloginlog/list")
def userloginlog_list():
    return render_template("admin/userloginlog_list.html")


# 添加权限
@admin.route("/auth/add")
def auth_add():
    return render_template("admin/auth_add.html")


# 权限列表
@admin.route("/tag/list")
def auth_list():
    return render_template("admin/auth_list.html")


# 添加角色
@admin.route("/role/add")
def role_add():
    return render_template("admin/role_add.html")


# 角色列表
@admin.route("/role/list")
def role_list():
    return render_template("admin/role_list.html")


# 添加管理员
@admin.route("/admin/add")
def admin_add():
    return render_template("admin/admin_add.html")


# 管理员列表
@admin.route("/admin/list")
def admin_list():
    return render_template("admin/admin_list.html")