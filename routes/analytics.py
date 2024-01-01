from flask import Blueprint, request, jsonify
from database.connection import get_db_connection
from sklearn.linear_model import LinearRegression
import traceback
import numpy as np

db_connection = get_db_connection()

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/predict_future_quiz_scores', methods=['GET'])
def predict_future_quiz_scores():
    try:
        mcqaccuracy_percentage_list = []
        timeaccuracy_percentage_list = []
        quiztimetaken_percentage_list = []
        data = fetch_user_data_from_database(request.get_json().get('uuid'))
        for quiz_attempt in data:
            mcqaccuracy_percentage_list.append(quiz_attempt[0])
            timeaccuracy_percentage_list.append(quiz_attempt[1])
            quiztimetaken_percentage_list.append(quiz_attempt[2])

        # Calculate average accuracy, average time taken, and average quiztimetaken
        average_accuracy = sum(mcqaccuracy_percentage_list) / \
            len(mcqaccuracy_percentage_list)
        average_time_taken = sum(
            timeaccuracy_percentage_list) / len(timeaccuracy_percentage_list)
        average_quiztimetaken = sum(
            quiztimetaken_percentage_list) / len(quiztimetaken_percentage_list)

        # Prepare data for linear regression
        X = np.array(timeaccuracy_percentage_list).reshape(-1, 1)
        y_accuracy = mcqaccuracy_percentage_list

        # Train linear regression model
        model_accuracy = LinearRegression()
        model_accuracy.fit(X, y_accuracy)

        # Predict future accuracy for 5 quizzes and 10 quizzes
        future_accuracy_5_quizzes = model_accuracy.predict(
            [[average_time_taken * 1.5]])[0]
        future_accuracy_10_quizzes = model_accuracy.predict(
            [[average_time_taken * 2.5]])[0]

        # Prepare response
        response = {
            "average_accuracy": average_accuracy,
            "average_time_accuracy": average_time_taken,
            "average_quiztimetaken": average_quiztimetaken,
            "predicted_accuracy_5_quizzes": future_accuracy_5_quizzes,
            "predicted_accuracy_10_quizzes": future_accuracy_10_quizzes
        }

        return jsonify(response)

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)})


def fetch_user_data_from_database(user_uuid):
    # Implement your database query logic here
    # Example: Fetching mcq_accuracy and time_accuracy for a user
    query = "SELECT mcqaccuracy, timeaccuracy, timetaken FROM user_attempted_quiz WHERE uuid = %s"
    with db_connection.cursor() as cursor:
        cursor.execute(query, (user_uuid,))
        user_data = cursor.fetchall()
    return user_data
