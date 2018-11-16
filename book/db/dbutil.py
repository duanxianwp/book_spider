from peewee import *
from book.db.redisutil import *
from playhouse.db_url import connect
import time


# 判断书是否已存在
def is_exist(url):
    db = DBHelper()
    return db.is_exist(url)


def is_no_exist(no):
    db = DBHelper()
    return db.is_no_exist(no)


def is_exist_isbn(isbn):
    db = DBHelper()
    return db.is_exist_isbn(isbn)


# 查出所有的可用用户
def get_all_able_user():
    db = DBHelper()
    return db.get_all_able_user()


#db = MySQLDatabase(settings.MYSQL_DATABASE, user=settings.MYSQL_USERNAME, passwd=settings.MYSQL_PASSWORD,
#                   host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, charset='utf8')
db = connect("mysql+pool://{}:{}@{}:{}/{}?charset=utf8&max_connections=20&stale_timeout=300".format(settings.MYSQL_USERNAME,settings.MYSQL_PASSWORD,settings.MYSQL_HOST,settings.MYSQL_PORT,settings.MYSQL_DATABASE))

class Base_Model(Model):
    class Meta:
        database = db


class Book_Detail(Base_Model):
    book_name = CharField()
    author = CharField()
    translator = CharField()
    editor = CharField()
    price = CharField()
    isbn = CharField()
    publish_status = CharField()
    publish_date = CharField()
    origin_book_name = CharField()
    origin_book_price = CharField()
    pages = CharField()
    format = CharField()
    introduction = CharField()
    origin_book_isbn = CharField()
    avatar = CharField()
    tags = CharField()
    book_url = CharField()
    website = CharField()

    # class Meta:
    #     database = settings.MYSQL_TABLE


class Bus(Base_Model):
    title = CharField()
    no = CharField()
    publish_date = CharField()
    time = CharField()
    maker = CharField()
    category = CharField()
    actors = CharField()
    photo = CharField()
    magent = CharField()
    url = CharField()


class User(Base_Model):
    name = CharField()
    phone = CharField()
    email = CharField()
    status = IntegerField()


class DBHelper(object):

    @staticmethod
    def update_data(data):

        if is_exist(data.get('book_url')) and is_exist_isbn(data.get('isbn')):
            return
        book = Book_Detail(book_name=data.get('book_name'),
                           author=data.get('author'), translator=data.get('translator'),
                           editor=data.get('editor'), price=data.get('price'),
                           isbn=data.get('isbn'), publish_status=data.get('publish_status'),
                           publish_date=data.get('publish_date'), origin_book_name=data.get('origin_book_name'),
                           origin_book_price=data.get('origin_book_price'), pages=data.get('pages'),
                           format=data.get('format'), introduction=data.get('introduction'),
                           origin_book_isbn=data.get('origin_book_isbn'), avatar=data.get('avatar'),
                           tags=data.get('tags'), book_url=data.get('book_url'), website=data.get('website'))
        try:
            book.save()
            # 存储数据到redis队列中
            lpush(data)
        except Exception as e:
            # print(e)
            # print(data)
            pass

    @staticmethod
    def is_exist(url):
        res = Book_Detail.select().where(Book_Detail.book_url == url)
        if res:
            return True
        else:
            return False

    @staticmethod
    def is_no_exist(no):
        res = Bus.select().where(Bus.no == no)
        if res:
            return True
        else:
            return False

    @staticmethod
    def is_exist_isbn(isbn):
        if isbn is None:
            return False
        res = Book_Detail.select().where(Book_Detail.isbn == isbn)
        if res:
            return True
        else:
            return False

    @staticmethod
    def get_today_books():
        date = time.time()
        date = date - date%86400
        Book_Detail.select().where(Book_Detail.update > date)

    @staticmethod
    def get_all_able_user():
        res = User.select().where(User.status == 1)
        if res:
            return res
        else:
            raise Exception("users is None")

    @staticmethod
    def insert_movie(data):
        if is_no_exist(data.get('no')):
            return
        bus = Bus(title=data.get('title'),
                  no=data.get('no'), publish_date=data.get('publish_date'),
                  time=data.get('time'), maker=data.get('maker'),
                  category=data.get('category'), actors=data.get('actors'),
                  photo=data.get('photo'), magent=data.get('magent'),
                  url=data.get("url"))
        try:
            bus.save()
        except Exception as e:
            # print(e)
            # print(data)
            pass
