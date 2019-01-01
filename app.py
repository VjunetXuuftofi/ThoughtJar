from flask import Flask
from flask import request
from flask import jsonify
import redis
from flask_cors import CORS
import os

r = redis.from_url(os.environ["REDIS_URL"])
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


@app.route('/add_sonya', methods=["POST"])
def add_sonya():
    return add("sonya")


@app.route('/get_sonya')
def get_sonya():
    return get("thomas")

@app.route('/add_thomas', methods=["POST"])
def add_thomas():
    return add("thomas")

@app.route('/get_thomas')
def get_thomas():
    return get("sonya")


@app.route('/get_count_sonya')
def get_count_sonya():
    return jsonify({"count": r.scard("thomas")})

@app.route('/get_count_thomas')
def get_count_thomas():
    return jsonify({"count": r.scard("sonya")})


if __name__ == '__main__':
    app.run()
