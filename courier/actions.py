import sys
import os
from getpass import getpass

from dotenv import load_dotenv
from redis import Redis
from bcrypt import hashpw, gensalt, checkpw


load_dotenv()
REST_API_URL = os.getenv("REST_API_URL")

DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NUMBER = os.getenv("DB_NUMBER")
db = Redis(host=DB_HOST, password=DB_PASSWORD, db=DB_NUMBER)


def start_register():
    print('\n')
    print('Sign Up')
    print('Enter your credentials\n')
    firstname = input("First Name: ")
    lastname = input("Last Name: ")
    username = input("Username: ")
    email = input("Email: ")
    password = getpass("Password: ")
    password1 = getpass("Repeat Password: ")

    firstname = str(firstname)
    lastname = str(lastname)
    username = str(username)
    email = str(email)
    password = str(password)
    password1 = str(password1)
    register(firstname, lastname,
             username, email, password, password1)


def register(firstname, lastname, username, email, password, password1):
    if not firstname or not lastname or not username or not email or not password or not password1:
        print('You passed empty values during registration')
        sys.exit(0)
    if len(username) < 3 or len(username) > 12:
        print('Length of username must be between 3 and 12')
        sys.exit(0)
    if len(password) < 8:
        print('Length of password must be at least 8 ')
        sys.exit(0)
    if password != password1:
        print('Passwords must be equal')
        sys.exit(0)

    if firstname and lastname and username and email and password and password1:
        if db.hexists(f"courier:{username}", "password"):
            print(f"Courier name: {username} is taken")
            sys.exit(0)

    password = password.encode()
    salt = gensalt(6)
    hashed = hashpw(password, salt)

    db.hset(f"courier:{username}", "firstname", firstname)
    db.hset(f"courier:{username}", "lastname", lastname)
    db.hset(f"courier:{username}", "email", email)
    db.hset(f"courier:{username}", "password", hashed)

    print(f'Welcome on board!')


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
