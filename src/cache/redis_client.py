import redis
from redis.exceptions import ConnectionError
import constant as cs
import jwt
import logging
import os

rds = redis.Redis(host=cs.REDIS_HOST, port=cs.REDIS_PORT, password=cs.REDIS_PWD, db=cs.REDIS_DB, socket_timeout=3000)

def get_redis_client():
    return redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

def rds_hmset(key, value, expire=3600):
    try:
        rds.set(key, value)
        rds.expire(key, expire)
    except redis.ConnectionError as e:
        logging.error(f"Redis connection error: {e}")

def make_token(email, _id):
    try:
        token = jwt.encode({"_id": _id, "email": email}, os.environ.get('JWT_SECRET', 'secret'), algorithm="HS256")
        return token
    except Exception as e:
        logging.error(f"Token generation error: {e}")
        return None

def delete_token(email):
    try:
        rds.delete(email)
    except redis.ConnectionError as e:
        logging.error(f"Redis connection error: {e}")

def deco_update(func):
    def wrapper(*args, **kwargs):
        val = func(*args, **kwargs)
        n_val = val[1]
        if not n_val:
            return val
        o_val = rds.hgetall(kwargs['key'])
        if o_val:
            for k in o_val:
                if k in n_val and n_val[k] and o_val[k] != n_val[k]:
                    o_val[k] = n_val[k]
            rds.hmset(kwargs['key'], o_val)
        return None, n_val

    return wrapper