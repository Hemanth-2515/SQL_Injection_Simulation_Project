from flask import Flask, render_template, request
import mysql.connector
import re

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host': "localhost",
    'user': "root",
    'port': "3306",
    'password': "sreyas123",
    'database': "sql-injection-sim"
}

def connect_db():
    return mysql.connector.connect(**db_config)

# Function to validate inputs
def validate_input(username, password):
    # Only allow alphanumeric characters for username and password
    if re.match("^[a-zA-Z0-9_]*$", username) and re.match("^[a-zA-Z0-9_]*$", password):
        return True
    return False

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle login POST request
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if not validate_input(username, password):
        return render_template('result.html', user_valid=False, error_msg="Invalid input.")

    try:
        db = connect_db()
        cursor = db.cursor()

        # Parameterized query to prevent SQL injection
        query = "SELECT * FROM users WHERE username = %s AND password1 = %s"
        cursor.execute(query, (username, password))
        user_result = cursor.fetchone()

        if user_result:
            # If login is successful, fetch users1 table data
            cursor.execute("SELECT users_id, user_pass, user_type, account_balance FROM users1")
            users1_data = cursor.fetchall()
            return render_template('result.html', user_valid=True, users1_data=users1_data)
        else:
            # If login fails, return error message
            return render_template('result.html', user_valid=False, error_msg="User ID or password is invalid.")

    except mysql.connector.Error as err:
        print("Error executing query:", err)
        return render_template('result.html', user_valid=False, error_msg="Database error occurred.")
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
