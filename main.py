import os
from cryptography.fernet import Fernet
import json

try:
    with open(os.environ['HOME']+"/passwrdman_key") as f:
        key = f.read().encode()
        secure = Fernet(key)
except FileNotFoundError: pass

try:
    with open(os.environ['HOME']+"/passwrdman_database") as f:
        database = json.loads(secure.decrypt(f.read()))
except FileNotFoundError:
    print("No Database Found")
    create_one = input("Create a database? (Y/n): ").lower()
    key = Fernet.generate_key()
    print(f"Your key is: {key}\nThis password is used to decrypt and encypt data.")
    secure = Fernet(key)
    if create_one.startswith('y'):
        with open(os.environ['HOME']+"/passwrdman_database", 'w') as f:
            f.write(secure.encrypt(json.dumps({"tokens": [], "passwords": []}).encode()).decode())
            database = {"tokens": [], "passwords": []}
        with open(os.environ['HOME']+"/passwrdman_key", 'w') as f:
            f.write(key.decode())
    elif create_one.startswith('n'):
        print("You do not have a database, so you can't use PasswrdMan.")
        exit(1)
    else:
        print("Unknown Option")
        exit(1)

option = input(f"Welcome, {os.getlogin().capitalize()}.\n1: Add Token\n2: Add Password\n3: Retrive Token\n4: Retrive Password\nEnter option: ")
try:
    option = int(option)
except ValueError:
    print("OPTION NOT STRING")
    exit(1)

if option == 1:
    token_name = input("Enter token name: ")
    token_value = input("Enter token value: ")
    project_name = input("Enter project name: ")
    database['tokens'].append({"name": token_name, "value": token_value, "project": project_name})
    with open(os.environ['HOME']+"/passwrdman_database", 'w') as f:
        f.write(secure.encrypt(json.dumps(database).encode()).decode())

if option == 2:
    username = input("Enter username for the password: ")
    password_name = input("Enter password name: ")
    password_value = input("Enter password value: ")
    URL = input("Enter website URL: ")
    database['passwords'].append({"name": password_name, "value": password_value, "URL": URL, "username": username})
    with open(os.environ['HOME']+"/passwrdman_database", 'w') as f:
        f.write(secure.encrypt(json.dumps(database).encode()).decode())

elif option == 3:
    query = input("Enter a string that must be in a token's name to include in the search results (case insensitive): ")
    for token in database['tokens']:
        if query in token['name'].lower():
            print('--------------------------')
            print("Token Name:", token['name'])
            print("Token Value:", token['value'])
            print("Token Project:", token['project'])

elif option == 4:
    query = input("Enter a string that must be in a password's name to include in the search results (case insensitive): ")
    for password in database['passwords']:
        if query in password['name'].lower():
            print('--------------------------')
            print('Username: ', password['username'])
            print("Password Name:", password['name'])
            print("Password Value:", password['value'])
            print("Website URL:", password['URL'])