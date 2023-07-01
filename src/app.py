__author__ = "Hiren Vasoya"
__date__ = "2023-06-06"
__version__ = '1.0.0'

import time
import os
import redis
import uuid
import jwt

from redis.exceptions import ConnectionError
from flask import Flask, request, jsonify
from models import users  # call model file
from flask_cors import CORS  # to avoid cors error in different frontend like react js or any other
import constant as cs

app = Flask(__name__)
CORS(app)

rds = redis.StrictRedis(host=cs.REDIS_HOST, port=cs.REDIS_PORT, password=cs.REDIS_PWD, db=cs.REDIS_DB, socket_timeout=3000)
rds_token = 'token:{}'.format


users = users.Users()

# user routes
def allowed_file(filename):
    tail = filename and '.' in filename and filename.rsplit('.', 1)[1]
    if tail and tail.lower() in cs.ALLOWED_EXTENSIONS:
        return tail
    else:
        return False


@app.route('/upload/<string:user_id>/', methods=['POST'])
def upload_file(user_id):
    name = request.values.get('filename')
    file = request.files['file']
    tail = allowed_file(file.filename)
    if file and tail:
        now = int(time.time())
        filename = name + '_' + str(now) + '.%s' % tail
        file.save(os.path.join('D:\python_mongodb\public', filename))
        response = users.updateOne(user_id, {'profile': filename})
        return jsonify(response), 200
    else:
        return jsonify({}), 200


@app.route('/users/login', methods=['POST'])
def login_user():
    if request.method == "POST":
        email = request.json.get('email')
        password = request.json.get('password')
        res = users.find_one({'email': email,'password': password});
        if res:
            print('res----',res)
            token = make_token(email)
            # rds_hmset(rds_token(token), first2dict({"email":email}))
            return jsonify({"token": token, "username": email}), 200

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users.find({})), 200


@app.route('/users/fetch/<string:user_id>/', methods=['GET'])
def get_user(user_id):
    return users.find_by_id(user_id), 200


@app.route('/users/cretae', methods=['POST'])
def add_users():
    if request.method == "POST":
        object = {
            'name': request.json.get('name'),
            'email': request.json.get('email'),
            'mobile': request.json.get('mobile'),
            'password': request.json.get('password'),
            'dob': request.json.get('dob')
        }

        print('object----',object)

        response = users.create(object)
        return response, 201


@app.route('/users/update/<string:user_id>/', methods=['PUT'])
def update_tasks(user_id):
    if request.method == "PUT":
        print('request.json---',user_id,request.json)
        name = request.json.get('name')
        mobile = request.json.get('mobile')
        response = users.update(user_id, {'name': name, 'mobile': mobile})
        return response, 201

@app.route('/users/delete/<string:user_id>/', methods=['DELETE'])
def delete_tasks(user_id):
    if request.method == "DELETE":
        users.delete(user_id)
        return "Record Deleted"


# redis

def rds_hmset(key, value, expire=3600):
    rds.hset(key, value)
    rds.expire(key, expire)


def make_token(email):
    token = jwt.encode({"email": email}, "secret", algorithm="HS256")
    return token


def delect_token(username):
    match = "token:*%s" % username
    result = rds.scan_iter(match=match, count=10000)
    for key in result:
        if rds.hget(key, 'username') == username:
            rds.delete(key)


def verify_token(token):
    pass


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


def first2dict(db_obj):
    new_dict = dict()
    # print("db_obj:",type(db_obj),db_obj.keys())   # 'Truck' object has no attribute 'keys'
    if hasattr(db_obj, "keys") and callable(db_obj.keys):  # callable(getattr(db_obj ,'keys'))
        for k in db_obj.keys():
            try:
                if hasattr(db_obj, k):
                    new_dict[k] = getattr(db_obj, k)
                else:
                    new_dict[k] = None
            except TypeError:
                new_dict[k] = None
    else:
        new_dict = vars(db_obj)
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
    return new_dict


if __name__ == '__main__':
    app.run(debug=True)
