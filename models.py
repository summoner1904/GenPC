from fuzzywuzzy import process
from app import db, app, manager
from flask_login import UserMixin


class BaseModel:
    """
    Класс, представляющий основные методы для работы с Базой Данных.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    name = db.Column(db.String(32))
    login = db.Column(db.String(32))
    def add(self) -> None:
        """
        Выполняет добавление сущности (объекта) в базу данных,
        после чего сохраняет изменения.
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create(cls, *args, **kwargs) -> None:
        """
        Создает новый объект нужного класса, при этом автоматически
        производит добавление в базу данных и возвращает созданный
        объект.
        :param args: user_id: int(Идентификатор пользователя)
        :param kwargs: request.form: dict(Словарь с данными из формы)
        :return: None
        """
        new_object = cls(*args, **kwargs)
        new_object.add()


class User(db.Model, UserMixin, BaseModel):
    """
    Класс, предоставляющий модель для хранения данных пользователя.
    """
    password = db.Column(db.String(32))


class Support(db.Model, BaseModel):
    """
    Класс, предоставляющий модель для хранения обращений пользователей в поддержку.
    """

    user_id = db.Column(db.Integer)
    message = db.Column(db.Text)


class Order(db.Model, BaseModel):
    """
    Класс, предоставляющий модель для хранения данных о сборках ПК пользователя.
    """

    user_id = db.Column(db.Integer)
    gpu = db.Column(db.String(32))
    cpu = db.Column(db.String(32))
    power = db.Column(db.String(32))
    motherboard = db.Column(db.String(32))
    ram = db.Column(db.String(32))
    storage = db.Column(db.String(32))


class Product(db.Model, BaseModel):
    """
    Класс, предоставляющий модель для хранения данных о комплектующих.
    """

    title = db.Column(db.String(64))
    description = db.Column(db.Text)
    price = db.Column(db.String(64))

    @classmethod
    def search(cls, searchbar):
        """
        Метод используется для поиска комплектующих в базе данных.
        :param searchbar: str(поисковый запрос пользователя)
        :return: result: list(список с найденными элементами в базе данных)
        """
        choices = list(map(lambda i: i.description, cls.query.all()))
        filter = process.extract(choices=choices, query=searchbar)
        result = []
        for i in filter:
            if i[1] > 50:
                result_search = cls.query.filter_by(description=i[0]).all()
                result.append(*result_search)
        return result


class Callback(db.Model, BaseModel):
    """
    Класс для сохранения заявок пользователей в базе данных.
    """
    phone = db.Column(db.String(32))


with app.app_context():
    db.create_all()


@manager.user_loader
def load_user(user_id):
    """
    Функция для flask_login.
    :param user_id: int (id пользователя)
    :return: Users (класс пользователя)
    """
    return User.query.get(user_id)
