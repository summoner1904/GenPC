import re
from fuzzywuzzy import process
from app import *
from models import Users, Support, Orders, Products
from errors import *


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        return redirect(url_for('result_of_search'))
    return render_template("index.html")


@app.route("/result/", methods=["POST", "GET"])
def result_of_search():
    return render_template(
        "result_of_search.html", result=Products.search(**dict(request.form))
    )


@app.route("/sign_in/", methods=["POST", "GET"])
def sign_in():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        user = Users.query.filter_by(login=login, password=password).first()
        if user:
            flash(
                {"title": "Успешно!", "message": "Вы успешно вошли в аккаунт!"},
                category="success",
            )
            login_user(user)
            return redirect(url_for("cabinet"))
        else:
            flash(
                {"title": "Ошибка!", "message": "Проверьте введенные данные!"},
                category="error",
            )
    return render_template("sign_in.html")


@app.route("/sign_up/", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        if check_data(**dict(request.form)):
            Users.create(**dict(request.form))
            flash(
                {"title": "Успешно!", "message": "Вы успешно зарегистрировались!"},
                category="success",
            )
            return redirect(url_for("sign_in"))
    return render_template("sign_up.html")


@app.route("/contacts/", methods=["POST", "GET"])
@login_required
def contacts():
    if request.method == "POST":
        Support.create(user_id=current_user.id, **dict(request.form))
        flash(
            {"title": "Успешно!", "message": "Ваше обращение до нас дошло."},
            category="success",
        )
    return render_template("contacts.html")


@app.route("/cabinet/", methods=["POST", "GET"])
@login_required
def cabinet():
    if request.method == "POST":
        email = request.form.get('email')
        if check_correct_email(email):
            current_user.email = email
            Users.add(current_user)
            flash(
                {"title": "Успешно!", "message": "Вы успешно изменили данные!"},
                category="success",
            )
        else:
            flash(
                {
                    "title": "Ошибка!",
                    "message": "Проверьте корректность введенных данных.",
                },
                category="error",
            )
    return render_template("cabinet.html")


pattern_login = r"^[a-z0-9]+$"
pattern_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$"


def check_correct_email(email):
    if email != current_user.email:
        if re.match(pattern_email, email) is None:
            return flash(
                {"title": "Ошибка!", "message": "Некорректная почта."}, category="error"
            )
        else:
            return True
    else:
        return flash(
            {"title": "Ошибка!", "message": "Вы ввели нынешний адрес."}, category="error"
        )


def check_data(login, email, password):

    if re.match(pattern_email, email) is None:
        return flash(
            {"title": "Ошибка!", "message": "Некорректная почта."}, category="error"
        )
    elif Users.query.filter_by(login=login).first():
        return flash(
            {"title": "Ошибка!", "message": "Такой логин уже есть в системе."},
            category="error",
        )
    elif Users.query.filter_by(email=email).first():
        return flash(
            {"title": "Ошибка!", "message": "Такая почта уже есть в системе."},
            category="error",
        )
    elif re.match(pattern_login, login) is None:
        return flash(
            {"title": "Ошибка!", "message": "Некорректный логин."}, category="error"
        )
    elif len(password) < 4 or len(password) > 32:
        return flash(
            {
                "title": "Ошибка!",
                "message": "Пароль должен быть не менее 4 и не более 32 символов.",
            },
            category="error",
        )
    else:
        return True


@app.route("/configurator/", methods=["POST", "GET"])
def configurator():
    if request.method == "POST":
        Orders.create(user_id=current_user.id, **dict(request.form))
    return render_template("configurator.html")


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("sign_in"))


@app.route("/add_database/", methods=["POST", "GET"])
def add_database():
    if request.method == "POST":
        title = request.form.get("title")
        price = int(request.form.get("price"))
        description = request.form.get("description")
        Products.create(title=title, price=price, description=description)
    return render_template("add_database.html")
