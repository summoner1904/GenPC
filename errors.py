from app import app
from flask import redirect, render_template, flash, url_for, Response


@app.errorhandler(401)
def error401(status: int) -> Response:
    """
    Функция обрабатывает ошибку HTTP 401, перенаправляя пользователя на страницу авторизации.
    :param status: int(Код ошибки)
    :return: None
    """
    flash(
        {"title": "Внимание!", "message": "Необходимо авторизоваться."}, category="info"
    )
    return redirect(url_for("sign_in")), 301


@app.errorhandler(404)
def error404(status: int) -> str:
    """
    Функция обрабатывает ошибку HTTP 404.
    :param status: int(Код ошибки)
    :return: error404.html (Шаблон страницы ошибки)
    """
    return render_template("errors/error404.html")


@app.errorhandler(429)
def error429(status: int) -> str:
    """
    Функция отрабатывает ошибку HTTP 429.
    :param status: int(Код ошибки)
    :return: error429.html (Шаблон страницы ошибки)
    Эта ошибка появляется, когда пользователь отправляет слишком много запросов
    (более 30 запросов в минуту).
    """
    return render_template("errors/error429.html")
