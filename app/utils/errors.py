from flask import jsonify

def error_response(message, status_code):
    return jsonify({'error': message}), status_code

def success_response(data, message="Success", status_code=200):
    return jsonify({'message': message, 'data': data}), status_code