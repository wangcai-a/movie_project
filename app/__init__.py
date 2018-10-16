from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = 'hard secret string'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:mysql@localhost:3306/movie'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.debug = True
db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")


# 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404