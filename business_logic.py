import re
from flask import flash
from models import Users
from flask_login import current_user

pattern_login = r"^[a-z0-9]+$"
pattern_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$"


def check_data(login, email, password) -> bool:
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


def check_new_user_data(email, old_password, new_password) -> bool:
    """
    Функция, использующаяся при проверки обновленных данных пользователя из личного кабинета
    :param email: str(Почта пользователя)
    :param old_password: str(Текущий пароль пользователя)
    :param new_password: str(Новый пароль пользователя)
    :return: Если данные корректны - True
            Если какие-то ошибки - False
    """
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