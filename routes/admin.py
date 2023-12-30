from flask import Blueprint, request, jsonify
from database.connection import get_db_connection
import hashlib
db_connection = get_db_connection()

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({'error': 'Missing username or password or email'}), 400

    try:
        hashed_password = hash_password(password)
        register_admin(username, hashed_password, email)
        return jsonify({'message': 'Admin registered successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    try:
        user_data = get_admin_data(username)
        if user_data == "Not admin":
            return jsonify({'error': 'Not admin'}), 401
        password = hash_password(password)
        print(password)
        print(user_data)
        if data and check_password(password, user_data['password']):
            return jsonify({'message': 'Login successful', 'uuid': user_data['uuid']}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def hash_password(password):
    # Use a strong hashing algorithm, such as SHA-256
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password


def get_admin_data(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        # check if admin or not
        results = cursor.fetchone()
        if results['adminstatus'] == 1:
            print(results)
            print("HEERE!@")
            return results
        else:
            return "Not admin"
    finally:
        cursor.close()
        conn.close()


def check_password(input_password, stored_password):
    # Verify the hashed input password against the stored hashed password
    return input_password == stored_password


def register_admin(username, password, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, uuid, email, adminstatus) VALUES (%s, %s, UUID(), %s, 1)", (username, password, email))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
