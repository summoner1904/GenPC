from app import app, render_template, redirect, url_for, flash


@app.errorhandler(401)
def error401(status):
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
def error404(status):
    """
    Функция обрабатывает ошибку HTTP 404.
    :param status: int(Код ошибки)
    :return: error404.html (Шаблон страницы ошибки)
    """
    return render_template("errors/error404.html")
