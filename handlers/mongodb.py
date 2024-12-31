import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class MongoDB:
    def __init__(self):
        self.client = MongoClient(os.getenv('DB'))
        self.db = self.client["bot_database"]
        self.collection = self.db["users"]

    def bind_profile(self, discord_id, user_id):
        update_data = {"$set": {"uid": user_id}}
        self.collection.update_one(
            {"_id": discord_id},
            update_data,
            upsert=True
        )

    def get_profile(self, discord_id):
        return self.collection.find_one({"_id": discord_id})

    def find_user_by_uid(self, uid):
        return self.collection.find_one({"uid": uid})

mongodb_handler = MongoDB()
