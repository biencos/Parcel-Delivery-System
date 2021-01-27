import os
import logging

from dotenv import load_dotenv
from redis import Redis
from flask import Flask, render_template
from flask_session import Session


load_dotenv()
REST_API_URL = os.getenv("REST_API_URL")

DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NUMBER = os.getenv("DB_NUMBER")
db = Redis(host=DB_HOST, password=DB_PASSWORD, db=DB_NUMBER)

SESSION_REDIS = db
SESSION_TYPE = 'redis'

app = Flask(__name__)
app.config.from_object(__name__)
ses = Session(app)
logging.basicConfig(level=logging.INFO)


# HOME
@app.route('/')
def load_home():
    return render_template("home.html")


# REGISTER
@app.route('/sender/register')
def load_register():
    # TODO
    return


@app.route('/sender/register', methods=['POST'])
def register():
    # TODO
    return


# LOGIN
@app.route('/sender/login')
def load_login():
    # TODO
    return


@app.route('/sender/login', methods=['POST'])
def login():
    # TODO
    return


if __name__ == '__main__':
    app.run()
