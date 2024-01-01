from database.connection import get_db_connection
connection = get_db_connection()


def createTables():
    with connection.cursor() as cursor:
        # Create User table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                uuid VARCHAR(255) PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                email VARCHAR(255),
                password VARCHAR(255),
                adminstatus boolean DEFAULT FALSE
            )
        ''')

        # Create Quiz table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz (
                quizId VARCHAR(255) PRIMARY KEY,
                uuid VARCHAR(255),
                quizType VARCHAR(255),
                quizSubject VARCHAR(255),
                quizTotalMcqs VARCHAR(255),
                quizExpectedTime VARCHAR(255),
                quizStartTime TIMESTAMP,
                FOREIGN KEY (uuid) REFERENCES users(uuid)
            )
        ''')

        # Create Mcqs table. Purely admin side.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Mcqs (
                mcqID VARCHAR(255) PRIMARY KEY,
                mcqSubject VARCHAR(255),
                mcqTitle VARCHAR(255),
                opt1 VARCHAR(255),
                opt2 VARCHAR(255),
                opt3 VARCHAR(255),
                opt4 VARCHAR(255),
                solution VARCHAR(255)
            )
        ''')

        # Create UserAttemptedQuiz table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_attempted_quiz (
                attemptID VARCHAR(255) PRIMARY KEY,
                uuid VARCHAR(255),
                quizId VARCHAR(255),
                quizEndtime TIMESTAMP,
                timetaken FLOAT,
                correctOptions INT,
                mcqaccuracy FLOAT,
                timeaccuracy FLOAT,
                FOREIGN KEY (uuid) REFERENCES users(uuid),
                FOREIGN KEY (quizID) REFERENCES quiz(quizID)
            )
        ''')

    # Commit the changes and close the connection
    connection.commit()
    connection.close()
