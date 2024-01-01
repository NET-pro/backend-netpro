from flask import Blueprint, request, jsonify
from database.connection import get_db_connection
import uuid as uuid_gen
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
    quiz_expected_time = (quiz_total_mcqs * 50)/60

    if not uuid or not quiz_type or not quiz_subject or not quiz_total_mcqs:
        return jsonify({'error': 'Missing required fields for quiz'}), 400

    quiz_id = str(uuid_gen.uuid4())  # Generate a unique ID for the quiz

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO quiz (quizId, uuid, quizType, quizSubject, quizTotalMcqs, quizExpectedTime, quizStartTime)
            VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        ''', (quiz_id, uuid, quiz_type, quiz_subject, quiz_total_mcqs, quiz_expected_time))
        conn.commit()
        return jsonify({'message': 'Quiz created successfully', 'quizid': quiz_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@quiz_bp.route('/submit_quiz', methods=['POST'])
def user_attempted_quiz():
    data = request.get_json()
    uuid = data.get('uuid')
    quiz_id = data.get('quizid')
    correct_options = data.get('correctOptions')
    print(data)
    if not uuid or not quiz_id or not correct_options:
        return jsonify({'error': 'Missing required fields for Submit quiz'}), 400

    # Generate a unique ID for the user's quiz attempt
    attempt_id = str(uuid_gen.uuid4())

    conn = get_db_connection()
    cursor = conn.cursor()
    # find the time started from quiz table
    cursor.execute('''
        SELECT * FROM quiz WHERE quizId = %s
    ''', (quiz_id,))
    result = cursor.fetchone()
    print(result)
    # quiz start time: datetime.datetime(2024, 1, 1, 4, 20, 37)
    quiz_start_time = result[6]
    # convert it
    quiz_start_time = datetime.strptime(
        str(quiz_start_time), '%Y-%m-%d %H:%M:%S')

    # calculate the time taken by the user
    quiz_end_time = datetime.now()
    print(quiz_end_time)
    print(quiz_start_time)
    print(((quiz_end_time - quiz_start_time).total_seconds())/60)
    timetaken = ((quiz_end_time - quiz_start_time).total_seconds())/60

    # calculate the mcq accuracy
    mcq_accuracy = (correct_options/float(result[4]))*100
    # calculate the time accuracy
    time_accuracy = (timetaken/float(result[5]))*100

    try:
        cursor.execute('''
            INSERT INTO user_attempted_quiz (attemptID, uuid, quizId, quizEndtime, timetaken, correctOptions, mcqaccuracy, timeaccuracy)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP , %s, %s, %s, %s)
        ''', (attempt_id, uuid, quiz_id, timetaken, correct_options, mcq_accuracy, time_accuracy))
        conn.commit()
        return jsonify({'message': 'User attempted quiz recorded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
