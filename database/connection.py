import mysql.connector


def get_db_connection():
    # Replace with your MySQL database credentials
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'database': 'netpro_db'
    }

    connection = mysql.connector.connect(**db_config)
    return connection
