import os
import logging

from dotenv import load_dotenv
from flask_hal import HAL
from flask import Flask, request, g
from redis import Redis
import jwt
from flask_hal.document import Document
from flask_hal.link import Link


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
