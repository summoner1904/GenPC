import uuid
import flask_monitoringdashboard as dashboard
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
    default_limits=["30 per minute"],
    storage_uri="memory://"
)
app.config["SECRET_KEY"] = str(uuid.uuid4())
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
toastr = Toastr(app)
manager = LoginManager(app)
dashboard.bind(app)
