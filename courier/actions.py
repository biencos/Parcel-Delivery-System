import sys
import os
from getpass import getpass
from datetime import datetime, timedelta

from dotenv import load_dotenv
from redis import Redis
from bcrypt import hashpw, gensalt, checkpw
import jwt
import requests


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
    print('\n')
    print('Sign in')
    print('Enter your login credentials \n')
    username = input("Your Username: ")
    password = getpass("Your Password: ")
    username = str(username)
    password = str(password)
    login(username, password)
    return username


def login(username, password):
    if not username or not password:
        print('You passed empty values during login process')
        sys.exit(0)
    if len(username) < 3 or len(username) > 12:
        print('Length of username must be between 3 and 12')
        sys.exit(0)
    if len(password) < 8:
        print('Length of password must be at least 8 ')
        sys.exit(0)

    if verify(username, password):
        print("\n")
        print(f"Welcome back courier: {username}")
        token = generate_jwt_token(username)
    else:
        print("Something went wrong! Was your credentials correct?")
        sys.exit(0)


def verify(username, password):
    p = password.encode()
    h = db.hget(f"courier:{username}", "password")

    if h:
        return checkpw(p, h)
    else:
        return False


def generate_jwt_token(username):
    USER_TYPE = 'courier'
    HOW_MANY_MINUTES_VALID = 10
    JWT_KEY = os.getenv("JWT_PRIVATE_KEY")
    if not username:
        return ''

    experience_date = datetime.utcnow() + timedelta(minutes=HOW_MANY_MINUTES_VALID)
    return jwt.encode({'username': username, 'exp': experience_date, 'usertype': USER_TYPE}, JWT_KEY, algorithm='HS256').decode()


# OPERATIONS ON COURIER REST API
# Get All Labels
# Add New Package
# Change Package Status
def start_getting_labels(username):
    print('\n')
    print('Show Labels for Courier')
    print('')
    get_courier_labels(f"{REST_API_URL}/courier/labels", username)


def get_courier_labels(url, username):
    h = generate_headers(generate_jwt_token(username))
    response = requests.get(url, headers=h)

    if response.json():
        body = response.json()
        if "message" in body:
            m = body["message"]
            print(m)
        if "labels" in body:
            labels = body["labels"]
            i = 1
            for label in labels:
                print(f"Label {i}")
                print("")
                print(f"Label ID: {label['label_id']}")
                print(f"Receiver Name: {label['receiver_name']}")
                print(f"Parcel Locker ID: {label['parcel_locker_id']}")
                print(f"Package Size: {label['package_size']}")
                if label['sent'] == "tak":
                    print("This package was sent.")
                else:
                    print("This package wasn't sent.")
                print("\n")
                i += 1
        else:
            print("Ups, Something went wrong. We weren't able to download your labels!")

    else:
        print("Ups, Something went wrong. We weren't able to download your labels!")
        sys.exit(0)


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


def generate_headers(token):
    headers = {}
    headers["Authorization"] = f"Bearer {token}"
    return headers
