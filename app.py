# app.py
from flask import Flask
from routes.user import user_bp
from routes.admin import admin_bp
from routes.mcqs import mcq_bp
from routes.quiz import quiz_bp
from routes.analytics import analytics_bp
from database.connection import get_db_connection
from database.tables import createTables

db_connection = get_db_connection()
createTables()

app = Flask(__name__)

# Register the user blueprint
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(mcq_bp, url_prefix='/mcq')
app.register_blueprint(quiz_bp, url_prefix='/quiz')
app.register_blueprint(analytics_bp, url_prefix='/analytics')


if __name__ == '__main__':
    app.run(debug=True)
