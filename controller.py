import re
from flask import request, abort
from flask_login import login_user, login_required, current_user, logout_user
from models import Users, Support, Orders, Products
from errors import *


@app.route("/", methods=["POST", "GET"])
def index():
    """
    Views главной страницы.
    :return: render_template(index.html)
    """
    if request.method == "POST":
        return redirect(url_for("result_of_search"))
    return render_template("index.html")


@app.route("/result/", methods=["POST", "GET"])
def result_of_search():
    """
    Views результатов поиска.
    :return: render_template(result_of_search)
    """
    return render_template(
        "result_of_search.html", result=Products.search(**dict(request.form))
    )


@app.route("/sign_in/", methods=["POST", "GET"])
def sign_in():
    """
    Функция, использующаяся для авторизации пользователей.
    :return: Если все данные верны, redirect(cabinet).
            Если данные неверные, просит ввести снова.
    """
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
    """
    Функция, использующаяся для регистрации пользователя.
    :return: Если все данные верны, сохраняет пользователя в БД, redirect(sign_in)
    """
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
    """
    Функция, использующаяся для обращений пользователей.
    :return: render_template(contacts)
    """
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
    """
    Views личного кабинета. Здесь можно изменить свои данные.
    :return: render_template(cabinet)
    """
    if request.method == "POST":
        if check_new_user_data(**dict(request.form)):
            Users.add(current_user)
            flash({"title": "Успешно!", "message": "Данные успешно изменены."}, category="success")
    return render_template('cabinet.html')


pattern_login = r"^[a-z0-9]+$"
pattern_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$"


def check_new_user_data(email, old_password, new_password):
    counter = 0
    if current_user.password == old_password:
        if email != '' and current_user.email != email:
            if re.match(pattern_email, email):
                counter += 1
                current_user.email = email
            else:
                return flash({"title": "Ошибка!", "message": "Некорректная почта."}, category="error")
        if new_password != '' and current_user.password != new_password:
            if 4 < len(new_password) < 32:
                current_user.password = new_password
                counter += 1
            else:
                return flash(
                    {
                        "title": "Ошибка!",
                        "message": "Пароль должен быть не менее 4 и не более 32 символов.",
                    },
                    category="error",
                    )
        if counter != 0:
            return True
    else:
        return flash({"title": "Ошибка!", "message": "Текущий пароль неверный."}, category="error")


def check_data(login, email, password):
    """
    Функция, использующаяся для проверки введенных пользователем данных для регистрации.
    :param login: str(Логин пользователя)
    :param email: str(Почта пользователя)
    :param password: str(Пароль пользователя)
    :return: Если возникла какая-то ошибка - False
            Если ошибок нет, данные корректны - True
    """
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
    """
    Views конфигуратора. После сборки в конфигураторе - создается запись в БД.
    :return: render_template(configurator)
    """
    if request.method == "POST":
        Orders.create(user_id=current_user.id, **dict(request.form))
    return render_template("configurator.html")


@app.route("/logout/")
def logout():
    """
    Функция, использующаяся для выхода из своего аккаунта пользователем.
    :return: redirect(sign_in)
    """
    logout_user()
    return redirect(url_for("sign_in"))


@app.route("/add_database/", methods=["POST", "GET"])
@login_required
def add_database():
    """
    Используется для добавления новых записей в базу данных.
    :return: render_template(add_database)
    """
    if current_user.login == "serjasum":
        if request.method == "POST":
            title = request.form.get("title")
            price = int(request.form.get("price"))
            description = request.form.get("description")
            Products.create(title=title, price=price, description=description)
        return render_template("add_database.html")
    else:
        return abort(404)
