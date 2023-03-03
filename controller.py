from __future__ import annotations
from business_logic import check_data, check_new_user_data
from flask import request, abort, render_template, redirect, flash, url_for, Response
from app import app
from flask_login import login_user, login_required, current_user, logout_user
from models import User, Support, Order, Product, Callback
from errors import error429, error404, error401


@app.route("/", methods=["POST", "GET"])
def index() -> Response | str:
    """
    Views главной страницы.
    :return: render_template(index.html)
    """
    if request.method == "POST":
        return redirect(url_for("result_of_search"))
    return render_template("index.html")


@app.route("/result/", methods=["POST"])
def result_of_search() -> str:
    """
    Views результатов поиска.
    :return: render_template(result_of_search)
    """
    return render_template(
        "result_of_search.html", result=Product.search(**dict(request.form))
    )


@app.route("/sign_in/", methods=["POST", "GET"])
def sign_in() -> Response | str:
    """
    Функция, использующаяся для авторизации пользователей.
    :return: Если все данные верны, redirect(cabinet).
            Если данные неверные, просит ввести снова.
    """
    if request.method == "GET":
        return render_template("sign_in.html")
    user = User.query.filter_by(**request.form).first()
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


@app.route("/sign_up/", methods=["POST", "GET"])
def sign_up() -> Response | str:
    """
    Функция, использующаяся для регистрации пользователя.
    :return: Если все данные верны, сохраняет пользователя в БД, redirect(sign_in)
    """
    if request.method == "GET":
        return render_template("sign_up.html")
    if check_data(**dict(request.form)):
        User.create(**dict(request.form))
        flash(
            {"title": "Успешно!", "message": "Вы успешно зарегистрировались!"},
            category="success",
        )
        return redirect(url_for("sign_in"))


@app.route("/contacts/", methods=["POST", "GET"])
@login_required
def contacts() -> str:
    """
    Функция, использующаяся для обращений пользователей.
    :return: render_template(contacts)
    """
    if request.method == "GET":
        return render_template("contacts.html")
    Support.create(user_id=current_user.id, **dict(request.form))
    flash(
        {"title": "Успешно!", "message": "Ваше обращение до нас дошло."},
        category="success",
    )


@app.route("/cabinet/", methods=["POST", "GET"])
@login_required
def cabinet() -> str:
    """
    Views личного кабинета. Здесь можно изменить свои данные.
    :return: render_template(cabinet)
    """
    if request.method == "POST":
        if check_new_user_data(**dict(request.form)):
            User.add(current_user)
            flash({"title": "Успешно!", "message": "Данные успешно изменены."}, category="success")
    orders = Order.query.filter_by(user_id=current_user.id)
    if orders:
        return render_template('cabinet.html', orders=orders)
    return render_template('cabinet.html')


@app.route("/configurator/", methods=["POST", "GET"])
def configurator() -> str:
    """
    Views конфигуратора. После сборки в конфигураторе - создается запись в БД.
    :return: render_template(configurator)
    """
    if request.method == "POST":
        flash({'title': 'Успешно!', 'message': 'Ваш компьютер ждет вас в личном кабинете!'}, category='success')
        Order.create(user_id=current_user.id, **dict(request.form))
    return render_template("configurator.html")


@app.route("/logout/")
def logout() -> Response:
    """
    Функция, использующаяся для выхода из своего аккаунта пользователем.
    :return: redirect(sign_in)
    """
    logout_user()
    return redirect(url_for("sign_in"))


@app.route("/add_database/", methods=["POST", "GET"])
@login_required
def add_database() -> Response | str:
    """
    Используется для добавления новых записей в базу данных. Доступно только администратору (логин serjasum).
    :return: render_template(add_database)
    """
    if current_user.login == "serjasum":
        if request.method == "POST":
            title = request.form.get("title")
            price = int(request.form.get("price"))
            description = request.form.get("description")
            Product.create(title=title, price=price, description=description)
        return render_template("add_database.html")
    else:
        return abort(404)


#  Константа, обозначающая, какую длину должен иметь номер телефона.
NUMBER_LENGTH = 11


@app.route('/oreon_pc/', methods=['POST', 'GET'])
def oreon_pc() -> str:
    """
    Views компьютера серии Oreon PC.
    :return: render_template(oreon)
    """
    if request.method == 'POST':
        if len(request.form.get('phone')) == NUMBER_LENGTH:
            Callback.create(**dict(request.form))
            flash({'title': 'Успешно!', 'message': 'Мы приняли вашу заявку. Ожидайте звонка.'}, category='success')
        else:
            flash({'title': 'Ошибка!', 'message': 'Вы ввели некорректный номер телефона.'}, category='error')
    return render_template('oreon.html')
