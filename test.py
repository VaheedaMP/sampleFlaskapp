from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


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
@app.route('/api/hello')
def hello():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
