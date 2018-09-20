from peewee import *
from book import settings


# 判断书是否已存在
def is_exist(url):
    db = DBHelper()
    return db.is_exist(url)


db = MySQLDatabase(settings.MYSQL_DATABASE, user=settings.MYSQL_USERNAME, passwd=settings.MYSQL_PASSWORD,
                   host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, charset='utf8')


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


class DBHelper(object):

    @staticmethod
    def update_data(data):
        if is_exist(data.get('book_url')):
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
        # 存储数据到redis队列中
        book.save()

    @staticmethod
    def is_exist(url):
        res = Book_Detail.select().where(Book_Detail.book_url == url)
        if res:
            return True
        else:
            return False
