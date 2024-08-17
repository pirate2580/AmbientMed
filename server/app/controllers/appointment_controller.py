from flask import Blueprint, request, jsonify, abort, send_file
from datetime import datetime
from io import BytesIO
from app.models.appointment_model import Appointment  # Import the Appointment model

# Define the Blueprint for the appointment controller
appointment_bp = Blueprint('appointment_bp', __name__)

# Initialize the model
appointment_model = Appointment()

@appointment_bp.route('/', methods=['POST'])
def create_appointment():
    data = request.form.to_dict()
    
    # Check for the video file in the request
    if 'video' in request.files:
        video_file = request.files['video']
        data['video'] = video_file.read()  # Read video file content as bytes
    
    # Convert the appointment_date from string to datetime object
    try:
        data['appointment_date'] = datetime.fromisoformat(data['appointment_date'])
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    appointment_id = appointment_model.create(data)
    return jsonify({'_id': appointment_id}), 201

@appointment_bp.route('/<id>', methods=['GET'])
def get_appointment(id):
    appointment = appointment_model.get_by_id(id)
    if appointment is None:
        abort(404)

    if 'video' in appointment:
        return send_file(BytesIO(appointment['video']), mimetype='video/mp4', as_attachment=True, download_name='appointment_video.mp4')
    
    appointment['_id'] = str(appointment['_id'])  # Convert ObjectId to string for JSON serialization
    return jsonify(appointment), 200

@appointment_bp.route('/', methods=['GET'])
def list_appointments():
    appointments = appointment_model.get_all()
    for appointment in appointments:
        appointment['_id'] = str(appointment['_id'])  # Convert ObjectId to string for JSON serialization
    return jsonify(appointments), 200

@appointment_bp.route('/<id>', methods=['PUT'])
def update_appointment(id):
    data = request.form.to_dict()
    
    if 'video' in request.files:
        video_file = request.files['video']
        data['video'] = video_file.read()  # Read video file content as bytes
    
    if 'appointment_date' in data:
        try:
            data['appointment_date'] = datetime.fromisoformat(data['appointment_date'])
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

    updated_count = appointment_model.update(id, data)
    if updated_count == 0:
        abort(404)
    return jsonify({'message': 'Appointment updated successfully'}), 200

@appointment_bp.route('/<id>', methods=['DELETE'])
def delete_appointment(id):
    deleted_count = appointment_model.delete(id)
    if deleted_count == 0:
        abort(404)
    return jsonify({'message': 'Appointment deleted successfully'}), 200
