"""File for appointment api routes and controlling routes"""

from flask import Blueprint, request, jsonify, abort, send_file
from datetime import datetime
from io import BytesIO
import os
from app.models.appointment_model import Appointment  # Import the Appointment model
from app.services.process_raw_file import transcribe_audio
from app.services.summarize import generate_soap
from dateutil.parser import parse as parse_date
# from app.services.summarize import generate_subjective, generate_objective, generate_assessment, generate_plan

# Define the Blueprint for the appointment controller
appointment_bp = Blueprint('appointment_bp', __name__)

appointment_model = Appointment()

@appointment_bp.route('/', methods=['POST'])
def create_appointment():
    # appointment
    # front end sends raw video to be processed by whisper and pyannote?
    data = request.form.to_dict() 

    video_file = request.files['video']

    transcription = transcribe_audio(video_file)
    processed_transcript = '\n\n'.join([f"[{segment['speaker']}] ({segment['segment_start']}-{segment['segment_end']}): {segment['segment_transcription']}" for segment in transcription])
    print(processed_transcript)
    result = generate_soap(processed_transcript)
    sections = result.split('<ENDOFSECTION>')
    print(sections)
    try:
        data['transcription'] = transcription
        data['video'] = video_file.read()
        data['subjective'] = sections[0]
        data['objective'] = sections[1]
        data['assessment'] = sections[2]
        data['plan'] = sections[3]
        data['appointment_name'] = 'Unnamed appointment'
        data['patient_name'] = "Unnamed patient"
        data['appointment_date'] = datetime.now()
        appointment_id = appointment_model.create(data)
        return jsonify({'_id': appointment_id}), 201
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500

@appointment_bp.route('/<id>', methods=['GET'])
def get_appointment(id):
    appointment = appointment_model.get_by_id(id)
    if appointment is None:
        abort(404)

    if 'video' in appointment:
        return send_file(BytesIO(appointment['video']), mimetype='video/mp4', as_attachment=False)
    
    appointment['_id'] = str(appointment['_id'])  # Convert ObjectId to string for JSON serialization
    return jsonify(appointment), 200

@appointment_bp.route('/all', methods=['GET'])
def list_appointments():
    appointments = appointment_model.get_all()
    for appointment in appointments:
        appointment['_id'] = str(appointment['_id'])  # Convert ObjectId to string for JSON serialization
    return jsonify(appointments), 200

@appointment_bp.route('/<id>', methods=['PUT'])
def update_appointment(id):
    data = request.get_json()
    print(data)
    # data = request.get_json()
    # appointment_name = data'appointmentName')
    # appointment_date = data.get('appointmentData')
    # patient_name = data.get('patientName')
    
    # if 'video' in request.files:
    #     video_file = request.files['video']
    #     data['video'] = video_file.read()  # Read video file content as bytes
    
    # if 'appointment_date' in data:
    #     try:
    # data['appointment_date'] = datetime.fromisoformat(data['appointment_date'])
    data['appointment_date'] = parse_date(data['appointment_date'])
        # except ValueError:
        #     return jsonify({'error': 'Invalid date format'}), 400

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
