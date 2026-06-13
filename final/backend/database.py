import os
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()

# MongoDB configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = "congo_shop"

async def connect_to_mongo(app):
    try:
        app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        app.mongodb = app.mongodb_client[DATABASE_NAME]
        print("Connected to MongoDB at", MONGO_URL)
    except Exception as e:
        print("Failed to connect to MongoDB:", e)
        app.mongodb_client = None
        app.mongodb = None

async def close_mongo_connection(app):
    if hasattr(app, "mongodb_client") and app.mongodb_client:
        app.mongodb_client.close()
        print("MongoDB connection closed.")
