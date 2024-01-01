# routes/user.py
from flask import Blueprint, request, jsonify
from database.connection import get_db_connection
import hashlib

db_connection = get_db_connection()

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({'error': 'Missing username or password or email'}), 400

    try:
        hashed_password = hash_password(password)
        register_user(username, hashed_password, email)
        return jsonify({'message': 'User registered successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    try:
        user_data = get_user_data(username)
        password = hash_password(password)

        if user_data and check_password(password, user_data['password']):
            return jsonify({'message': 'Login successful', 'uuid': user_data['uuid']}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


def register_user(username, password, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, uuid, email) VALUES (%s, %s, UUID(), %s)", (username, password, email))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def hash_password(password):
    # Use a strong hashing algorithm, such as SHA-256
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password


def get_user_data(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def check_password(input_password, stored_password):
    # Verify the hashed input password against the stored hashed password
    return input_password == stored_password
