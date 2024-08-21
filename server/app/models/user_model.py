import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

class User:
  def __init__(self):
      # Initialize the MongoDB client and select the database and collection
      load_dotenv()
      self.client = MongoClient(os.environ.get("MONGODB_URI"))
      self.db = self.client['AmbientMed']
      self.collection = self.db['Users']

  def create(self, data):
      # self.validate(data)
      result = self.collection.insert_one(data)
      return str(result.inserted_id)

  def get_by_email(self, email):

      user = self.collection.find_one({"email": email})
      return user

  def get_all(self):

      users = list(self.collection.find())
      return users

  def update(self, appointment_id, data):
      
      result = self.collection.update_one(
          {"_id": ObjectId(appointment_id)},
          {"$set": data}
      )
      return result.modified_count

  def delete(self, user_id):
      user = self.collection.find_one({"_id": ObjectId(user_id)})
      
      result = self.collection.delete_one({"_id": ObjectId(user_id)})
      return result.deleted_count
