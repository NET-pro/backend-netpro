from flask import Blueprint, request, jsonify
from database.connection import get_db_connection
import uuid
from datetime import datetime

db_connection = get_db_connection()

quiz_bp = Blueprint('quiz', __name__)


@quiz_bp.route('/create_quiz', methods=['POST'])
def create_quiz():
    data = request.get_json()
    uuid = data.get('uuid')
    quiz_type = data.get('quizType')
    quiz_subject = data.get('quizSubject')
    quiz_total_mcqs = data.get('quizTotalMcqs')
    quiz_expected_time = data.get('quizExpectedTime')

    if not uuid or not quiz_type or not quiz_subject or not quiz_total_mcqs or not quiz_expected_time:
        return jsonify({'error': 'Missing required fields for quiz'}), 400

    quiz_id = str(uuid.uuid4())  # Generate a unique ID for the quiz

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO quiz (quizId, uuid, quizType, quizSubject, quizTotalMcqs, quizExpectedTime, quizStartTime)
            VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        ''', (quiz_id, uuid, quiz_type, quiz_subject, quiz_total_mcqs, quiz_expected_time))
        conn.commit()
        return jsonify({'message': 'Quiz created successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@quiz_bp.route('/user_attempted_quiz', methods=['POST'])
def user_attempted_quiz():
    data = request.get_json()
    uuid = data.get('uuid')
    quiz_id = data.get('quizId')
    quiz_endtime = data.get('quizEndtime')
    timetaken = data.get('timetaken')
    correct_options = data.get('correctOptions')
    mcq_accuracy = data.get('mcqaccuracy')
    time_accuracy = data.get('timeaccuracy')

    if not uuid or not quiz_id or not quiz_endtime or not timetaken or not correct_options or not mcq_accuracy or not time_accuracy:
        return jsonify({'error': 'Missing required fields for user_attempted_quiz'}), 400

    # Generate a unique ID for the user's quiz attempt
    attempt_id = str(uuid.uuid4())

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO user_attempted_quiz (attemptID, uuid, quizId, quizEndtime, timetaken, correctOptions, mcqaccuracy, timeaccuracy)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (attempt_id, uuid, quiz_id, quiz_endtime, timetaken, correct_options, mcq_accuracy, time_accuracy))
        conn.commit()
        return jsonify({'message': 'User attempted quiz recorded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
