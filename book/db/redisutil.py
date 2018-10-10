import redis
from book import settings

pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                            db=settings.REDIS_DATABASE_INDEDX, password=settings.REDIS_PASSWORD)
r = redis.StrictRedis(connection_pool=pool)


def sadd(data):
    r.sadd("book", data)


def smembers():
    return r.smembers("book")


def spop():
    return r.spop("book")


def del_set():
    r.delete("book")
