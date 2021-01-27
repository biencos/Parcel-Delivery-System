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


@app.route('/sender/labels/<label_id>', methods=["DELETE"])
def delete_label(label_id):
    username = g.authorization.get("username")
    usertype = g.authorization.get("usertype")

    if not username or usertype != "sender":
        return make_response(
            {"message": "Log in as a sender to delete label", "status": "error"}, 401)

    if not label_id or not db.sismember(f"user:{username}:labels", label_id):
        return make_response(
            {"message": f"Incorrect label ID", "status": "error"}, 403)

    sent = db.hget(f"label:{label_id}", "sent").decode('utf-8')
    if not sent:
        return make_response(
            {"message": f"This label doesn't have sent status yet, weird", "status": "error"}, 403)

    if sent == "tak":
        return make_response(
            {"message": f"You can't delete label that was sent. Change label status, and then try again", "status": "error"}, 403)

    db.delete(f"label:{label_id}")
    db.srem(f"user:{username}:labels", label_id)

    response = {"message": "Label was deleted"}
    links = []
    document = Document(data=response, links=links)
    return document.to_json(), 200


@app.route('/sender/labels/<label_id>', methods=["PUT"])
def change_label_sent_status(label_id):
    username = g.authorization.get("username")
    usertype = g.authorization.get("usertype")

    if not username or usertype != "sender":
        return make_response(
            {"message": "Log in as a sender to change status of sent", "status": "error"}, 401)

    labels = db.keys(f"label:{label_id}")
    if not label_id or len(labels) == 0:
        return make_response(
            {"message": "Incorrect label ID", "status": "error"}, 403)

    sent = db.hget(f"label:{label_id}", "sent").decode('utf-8')
    if not sent:
        return make_response(
            {"message": f"This label doesn't have sent status yet", "status": "error"}, 403)

    if sent == "nie":
        db.hset(f"label:{label_id}", "sent", "tak")
    else:
        db.hset(f"label:{label_id}", "sent", "nie")
    db.sadd(f"user:{username}:labels", label_id)

    response = {"message": "Status of label was succesfully changed"}
    links = []
    document = Document(data=response, links=links)
    return document.to_json(), 200


# SENDER NOTIFICATIONS
@app.route('/sender/notifications', methods=["GET"])
def get_notifications():
    username = g.authorization.get("username")
    usertype = g.authorization.get("usertype")

    if not username or usertype != "sender":
        return make_response(
            {"message": "Log in as a sender to get notifications", "status": "error"}, 401)

    label_ids = list(db.smembers(f"user:{username}:labels"))
    for i, label_id in enumerate(label_ids):
        label_ids[i] = label_id.decode('utf-8')

    notifications = []
    for label_id in label_ids:
        if db.exists(f"notification:{label_id}"):
            notification = {}
            notification['label_receiver'] = db.hget(
                f"label:{label_id}", "receiver_name").decode('utf-8')
            notification['new_status'] = db.hget(
                f"notification:{label_id}", "new_status").decode('utf-8')

            notifications.append(notification)
            db.delete(f"notification:{label_id}")

    response = {}
    response['notifications'] = notifications
    links = []
    document = Document(data=response, links=links)
    return document.to_json(), 200


# COURIER
@app.route('/courier', methods=["GET"])
def get_courier():
    response = {}
    links = []
    links.append(Link('labels', '/courier/labels'))
    document = Document(data=response, links=links)
    return document.to_json(), 200


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
