import redis
from book import settings

pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                            db=settings.REDIS_DATABASE_INDEDX, password=settings.REDIS_PASSWORD)
r = redis.StrictRedis(connection_pool=pool)


def lpush(data):
    r.lpush("book", data)


def keys_num():
    return r.llen("book")


def lrange():
    return r.lrange("book", 0, keys_num())


def spop():
    return r.spop("book")


def del_set():
    r.delete("book")
