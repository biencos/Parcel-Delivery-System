import os
import logging

from dotenv import load_dotenv
from flask_hal import HAL
from flask import Flask, request, g, make_response
from redis import Redis
import jwt
from flask_hal.document import Document
from flask_hal.link import Link
from uuid import uuid4


load_dotenv()
JWT_KEY = os.getenv("JWT_PRIVATE_KEY")

DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NUMBER = os.getenv("DB_NUMBER")
db = Redis(host=DB_HOST, password=DB_PASSWORD, db=DB_NUMBER)


app = Flask(__name__)
HAL(app)
logging.basicConfig(level=logging.INFO)


@app.before_request
def before_request_func():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        g.authorization = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        logging.info("User authorized")
    except Exception as e:
        g.authorization = {}
        logging.info("There was an error, user wasn't authorized!")
        logging.info(str(e))


# SENDER
@app.route('/sender', methods=["GET"])
def get_sender():
    response = {}
    links = []
    links.append(Link('labels', '/sender/labels'))
    document = Document(data=response, links=links)
    return document.to_json(), 200


@app.route('/sender/labels', methods=["GET"])
def get_labels():
    username = g.authorization.get("username")
    usertype = g.authorization.get("usertype")

    if not username or usertype != "sender":
        return make_response(
            {"message": "Log in as a sender to get labels", "status": "error"}, 401)

    label_ids = list(db.smembers(f"user:{username}:labels"))
    for i, label_id in enumerate(label_ids):
        label_ids[i] = label_id.decode('utf-8')

    labels = []
    for label_id in label_ids:
        label = {}
        label['label_id'] = label_id
        label['receiver_name'] = db.hget(
            f"label:{label_id}", "receiver_name").decode('utf-8')
        label['parcel_locker_id'] = db.hget(
            f"label:{label_id}", "parcel_locker_id").decode('utf-8')
        label['package_size'] = db.hget(
            f"label:{label_id}", "package_size").decode('utf-8')
        label['sent'] = db.hget(
            f"label:{label_id}", "sent").decode('utf-8')

        labels.append(label)

    response = {}
    response['labels'] = labels
    links = []
    document = Document(data=response, links=links)
    return document.to_json(), 200


@app.route('/sender/labels', methods=["POST"])
def add_label():
    username = g.authorization.get("username")
    usertype = g.authorization.get("usertype")

    if not username or usertype != "sender":
        return make_response(
            {"message": "Log in as a sender to add label", "status": "error"}, 401)

    label_id = str(uuid4())
    receiver_name = request.form.get("receiver_name")
    parcel_locker_id = request.form.get("parcel_locker_id")
    package_size = request.form.get("package_size")
    sent = "nie"

    db.hset(f"label:{label_id}", "receiver_name", receiver_name)
    db.hset(f"label:{label_id}", "parcel_locker_id", parcel_locker_id)
    db.hset(f"label:{label_id}", "package_size", package_size)
    db.hset(f"label:{label_id}", "sent", sent)

    db.sadd(f"user:{username}:labels", label_id)

    response = {"message": "Label was added"}
    links = []
    links.append(Link('labels:DELETE', f'/sender/labels/{label_id}'))
    document = Document(data=response, links=links)
    return document.to_json(), 201


# HOME
@app.route('/', methods=["GET"])
def get_home():
    response = {}
    links = []
    links.append(Link('sender', '/sender'))
    links.append(Link('courier', '/courier'))
    document = Document(data=response, links=links)
    return document.to_json(), 200


if __name__ == '__main__':
    app.run()
