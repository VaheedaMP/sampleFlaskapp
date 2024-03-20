from flask import Flask, request, jsonify
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


@app.route('/add_employee', methods=['POST'])
def add_employee():
    logging.info('This is add_employee API')
    try:
        data = request.json
        name = data.get('name')
        position = data.get('position')

        if not name or not position:
            return jsonify({'error': 'Missing name or position in request'}), 400

        return jsonify({'message': 'Employee added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/employees', methods=['GET'])
def get_employees():
    logging.info('This is employees API')
    try:
        employee_list = [
            {'id': 1, 'name': 'John Doe', 'position': 'Software Engineer'},
            {'id': 2, 'name': 'Jane Smith', 'position': 'Data Analyst'},
        ]
        return jsonify(employee_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/hello')
def hello():
    logging.info('This is hello API')
    return jsonify({'message': 'Hello, World!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
