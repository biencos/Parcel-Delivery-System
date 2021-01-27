import os

from dotenv import load_dotenv
from redis import Redis


load_dotenv()
REST_API_URL = os.getenv("REST_API_URL")

DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NUMBER = os.getenv("DB_NUMBER")
db = Redis(host=DB_HOST, password=DB_PASSWORD, db=DB_NUMBER)


def start_register():
    # TODO
    return


def register(firstname, lastname, username, email, password, password1):
    # TODO
    return


def start_login():
    # TODO
    return


def login(username, password):
    # TODO
    return


# OPERATIONS ON COURIER REST API
# Get All Labels
# Add New Package
# Change Package Status
def start_getting_labels(username):
    # TODO
    return


def get_courier_labels(url, username):
    # TODO
    return


def start_adding_package(username):
    # TODO
    return


def add_package_from_label(url, username):
    # TODO
    return


def start_changing_package_status(username):
    # TODO
    return


def change_package_status(url, username):
    # TODO
    return
