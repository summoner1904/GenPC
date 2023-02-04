from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"] = "fAZmf248XfG"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
toastr = Toastr(app)
manager = LoginManager(app)
