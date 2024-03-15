from flask import Flask, request, jsonify
import sqlite3
import logging

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('C:/Users/Mobile Programming/sampleFlaskApp/app.log'),
        logging.StreamHandler()
    ]
)

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, position TEXT)''')
    conn.commit()
    conn.close()


# Initialize the database
init_db()


# Endpoint to add an employee
@app.route('/add_employee', methods=['POST'])
def add_employee():
    logging.info('This is add_employee API')
    try:
        data = request.json
        name = data['name']
        position = data['position']

        conn = sqlite3.connect('employees.db')
        c = conn.cursor()
        c.execute("INSERT INTO employees (name, position) VALUES (?, ?)", (name, position))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Employee added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/employees', methods=['GET'])
def get_employees():
    logging.info('This is employees API')
    try:
        conn = sqlite3.connect('employees.db')
        c = conn.cursor()
        c.execute("SELECT * FROM employees")
        employees = c.fetchall()
        conn.close()

        employee_list = []
        for employee in employees:
            employee_dict = {'id': employee[0], 'name': employee[1], 'position': employee[2]}
            employee_list.append(employee_dict)

        return jsonify(employee_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/hello')
def hello():
    logging.info('This is hello API')
    return jsonify({'message': 'Hello, World!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
