from flask import Blueprint, request, jsonify
from database.connection import get_db_connection

db_connection = get_db_connection()

mcq_bp = Blueprint('mcq', __name__)


def is_admin(uuid):
    with db_connection.cursor() as cursor:
        cursor.execute(
            'SELECT adminstatus FROM users WHERE uuid = %s', (uuid,))
        result = cursor.fetchone()
        # If result is not None and adminstatus is True
        return result and result[0]


@mcq_bp.route('/add_mcq', methods=['POST'])
def add_mcq():
    try:
        data = request.get_json()

        # Extracting data from the request
        uuid = data.get('uuid')
        mcq_subject = data.get('mcqSubject')
        mcq_title = data.get('mcqTitle')
        opt1 = data.get('opt1')
        opt2 = data.get('opt2')
        opt3 = data.get('opt3')
        opt4 = data.get('opt4')
        solution = data.get('solution')

        # Check if the user is an admin
        if not is_admin(uuid):
            return jsonify({"error": "User is not an admin"}), 403

        # Insert the MCQ into the database
        with db_connection.cursor() as cursor:
            cursor.execute('''
                INSERT INTO Mcqs (mcqID, mcqSubject, mcqTitle, opt1, opt2, opt3, opt4, solution)
                VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s)
            ''', (mcq_subject, mcq_title, opt1, opt2, opt3, opt4, solution))

        # Commit the changes and close the connection
        db_connection.commit()

        return jsonify({"message": "MCQ added successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@mcq_bp.route('/get_mcqs', methods=['GET'])
def get_mcqs():
    try:
        # Get parameters from the request
        # http://localhost:5000/mcq/get_mcqs?num_mcqs=5&subject=Math
        num_mcqs = int(request.args.get('num_mcqs', default=5))
        subject = request.args.get('subject')

        # Validate parameters
        if not subject:
            return jsonify({"error": "Subject is required"}), 400

        # Fetch MCQs from the database
        with db_connection.cursor() as cursor:
            cursor.execute('''
                SELECT * FROM Mcqs
                WHERE mcqSubject = %s
                ORDER BY RAND()
                LIMIT %s
            ''', (subject, num_mcqs))
            mcqs = cursor.fetchall()

        # Convert the result to a list of dictionaries
        mcqs_list = []
        for mcq in mcqs:
            mcq_dict = {
                "mcqID": mcq[0],
                "mcqSubject": mcq[1],
                "mcqTitle": mcq[2],
                "opt1": mcq[3],
                "opt2": mcq[4],
                "opt3": mcq[5],
                "opt4": mcq[6],
                "solution": mcq[7]
            }
            mcqs_list.append(mcq_dict)

        return jsonify({"mcqs": mcqs_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
