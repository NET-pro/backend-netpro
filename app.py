# app.py
from flask import Flask
from routes.user import user_bp
from database.connection import get_db_connection
from database.tables import createTables

db_connection = get_db_connection()
createTables()

app = Flask(__name__)

# Register the user blueprint
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)
