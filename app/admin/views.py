from . import admin
from flask import render_template, url_for, redirect


# 主页面
@admin.route("/")
def index():
    return render_template("admin/index.html")


# 登入
@admin.route("/login")
def login():
    return render_template("admin/login.html")


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


# 会员添加
@admin.route("/admin/add")
def admin_add():
    return render_template("admin/admin_add.html")


# 会员列表
@admin.route("/admin/list")
def admin_list():
    return render_template("admin/admin_list.html")


# 会员列表
@admin.route("/cmoment/list")
def comment_list():
    return render_template("admin/comment_list.html")

