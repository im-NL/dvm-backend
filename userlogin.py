import json

users = json.load(open("users.json"))

def login():

    user = input("Enter your username: ")
    pwd = input("Enter password: ")

    try:
        if users[user]["password"] == pwd:
            print("Login Complete")
            return [user, users[user], users]
        else:
            print("Invalid password")
    except KeyError:
        print("Invalid username")


