import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from gridfs import GridFS
# from datetime import datetime

class Appointment:
    def __init__(self):
        # Initialize the MongoDB client and select the database and collection
        load_dotenv()
        self.client = MongoClient(os.environ.get("MONGODB_URI"))
        self.db = self.client['AmbientMed']
        self.collection = self.db['Appointments']
        self.fs = GridFS(self.db)

    def create(self, data):
        # Check if video file is in data and save it to GridFS
        if 'video' in data and isinstance(data['video'], bytes):
            video_id = self.fs.put(data['video'], filename='appointment_video.mp4')
            data['video'] = video_id
        
        # Insert a new appointment document into the collection
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def get_by_id(self, appointment_id):
        appointment = self.collection.find_one({"_id": ObjectId(appointment_id)})
        
        # Retrieve the video from GridFS if it exists
        if appointment and 'video' in appointment:
            video_data = self.fs.get(appointment['video']).read()
            appointment['video'] = video_data
        
        return appointment

    def get_all(self):
        appointments = list(self.collection.find())
        
        # Retrieve videos from GridFS if they exist
        for appointment in appointments:
            if 'video' in appointment:
                video_data = self.fs.get(appointment['video']).read()
                appointment['video'] = video_data
        
        return appointments

    def update(self, appointment_id, data):
        if 'video' in data and isinstance(data['video'], bytes):
            video_id = self.fs.put(data['video'], filename='appointment_video.mp4')
            data['video'] = video_id
        
        result = self.collection.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": data}
        )
        return result.modified_count

    def delete(self, appointment_id):
        appointment = self.collection.find_one({"_id": ObjectId(appointment_id)})
        
        # Delete the video from GridFS if it exists
        if appointment and 'video' in appointment:
            self.fs.delete(appointment['video'])
        
        result = self.collection.delete_one({"_id": ObjectId(appointment_id)})
        return result.deleted_count
