from os import name
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash

app = Flask(name)

users = {}


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if username in users:
        return jsonify({"error": "Пользователь уже существует"}), 400

    users[username] = {
        "username": username,
        "email": email,
        "password": generate_password_hash(password)
    }

    return jsonify(users[username]), 201


@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    if username in users:
        user = users[username].copy()
        del user['password']
        return jsonify(user)
    else:
        return jsonify({"error": "Пользователь не найден"}), 404


if name == 'main':
    app.run(debug=True)