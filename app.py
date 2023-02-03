from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr
from flask_login import (
    UserMixin,
    logout_user,
    login_user,
    LoginManager,
    login_required,
    current_user,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "fAZmf248XfG"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
toastr = Toastr(app)
manager = LoginManager(app)
