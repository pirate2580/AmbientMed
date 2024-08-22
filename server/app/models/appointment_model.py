"""File for appointment model in MongoDB"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from gridfs import GridFS
from datetime import datetime

class Appointment:

    FIELDS = {
        'transcription': list,
        'video': bytes,
        'subjective': str,
        'objective': str,
        'assessment': str,
        'plan': str,
        'appointment_name': str,
        'appointment_date': datetime,
        'video_description': str,
    }

    def __init__(self):
        # Initialize the MongoDB client and select the database and collection
        load_dotenv()
        self.client = MongoClient(os.environ.get("MONGODB_URI"))
        self.db = self.client['AmbientMed']
        self.collection = self.db['Appointments']
        self.fs = GridFS(self.db)
    
    def validate(self, data):
        for field, field_type in self.FIELDS.items():
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
            if not isinstance(data[field], field_type):
                raise TypeError(f"Field '{field}' must be of type {field_type.__name__}")
        
        for field in data:
            if field not in self.FIELD:
                raise ValueError(f"Extra field: {field}")

    def create(self, data):
        # self.validate(data)

        # Check if video file is in data and save it to GridFS
        video_id = self.fs.put(data['video'], filename='appointment_video.mp4')
        data['video'] = video_id
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def get_by_id(self, appointment_id):
        appointment = self.collection.find_one({"_id": ObjectId(appointment_id)}, {"video": 0})
        transcript = appointment['transcript']
        # appointment = self.collection.find_one({"_id": ObjectId(appointment_id)})
        # Retrieve the video from GridFS if it exists
        # if appointment:
        #     video_data = self.fs.get(appointment['video']).read()
        #     appointment['video'] = video_data
        
        return appointment

    def get_all(self):

        appointments = list(self.collection.find({}, {"video": 0}))
        
        # Retrieve videos from GridFS if they exist
        # for appointment in appointments:
        #     video_data = self.fs.get(appointment['video']).read()
        #     appointment['video'] = video_data
        
        return appointments

    def update(self, appointment_id, data):
        # self.validate(data)

        # if isinstance(data['video'], bytes):
        #     video_id = self.fs.put(data['video'], filename='appointment_video.mp4')
        #     data['video'] = video_id
        
        result = self.collection.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": data}
        )
        return result.modified_count

    def delete(self, appointment_id):
        appointment = self.collection.find_one({"_id": ObjectId(appointment_id)})
        
        # Delete the video from GridFS if it exists
        if appointment:
            self.fs.delete(appointment['video'])
        
        result = self.collection.delete_one({"_id": ObjectId(appointment_id)})
        return result.deleted_count
