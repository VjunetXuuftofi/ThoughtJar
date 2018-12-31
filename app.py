from flask import Flask
from flask import request
from flask import jsonify
import redis
from flask_cors import CORS
import os

r = redis.Redis(host=os.environ["REDIS_URL"])
app = Flask(__name__)
CORS(app)


def add(name):
    thought = request.json["thought"]
    r.sadd(name, thought)
    r.sadd(name + "_alltime", thought)
    return jsonify({"success": True})

def get(name):
    value = r.srandmember(name)
    if value is None:
        response = jsonify({"thought": None, "error": "There are no thoughts left!"})
        return response, 404
    else:
        r.srem(name, value)
        return jsonify({"thought": value.decode("utf-8")})


@app.route('/add_Sonya', methods=["POST"])
def add_Sonya():
    return add("Sonya")


@app.route('/get_Sonya')
def get_Sonya():
    return get("Thomas")

@app.route('/add_Thomas', methods=["POST"])
def add_Thomas():
    return add("Thomas")

@app.route('/get_Thomas')
def get_Thomas():
    return get("Sonya")


@app.route('/get_count_Sonya')
def get_count_Sonya():
    return jsonify({"count": r.scard("Thomas")})

@app.route('/get_count_Thomas')
def get_count_Thomas():
    return jsonify({"count": r.scard("Sonya")})


if __name__ == '__main__':
    app.run()
