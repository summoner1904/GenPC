from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute", "5 per second"],
    storage_uri="memory://"
)
app.config["SECRET_KEY"] = "fAZmf248XfG"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
toastr = Toastr(app)
manager = LoginManager(app)
