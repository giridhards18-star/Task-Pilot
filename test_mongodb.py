#!/usr/bin/env python3
"""
Test script to verify MongoDB connection and basic operations
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import date

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://giridhards18_db_user:uAovwnOOK26qYUJo@taskpilot.xqvmkpd.mongodb.net/')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'taskpilot')

try:
    print("🔌 Connecting to MongoDB...")
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]

    # Test connection
    db.command('ping')
    print("✅ MongoDB connection successful!")

    # Get collections info
    collections = db.list_collection_names()
    print(f"📊 Available collections: {collections}")

    # Test user collection
    users_collection = db.users
    users_count = users_collection.count_documents({})
    print(f"👥 Users in database: {users_count}")

    # Test tasks collection
    tasks_collection = db.tasks
    tasks_count = tasks_collection.count_documents({})
    print(f"📝 Tasks in database: {tasks_count}")

    # Test inserting a sample user (if none exists)
    if users_count == 0:
        print("🆕 Creating sample user...")
        sample_user = {
            "username": "testuser",
            "password": "testpass",
            "created_at": date.today().isoformat()
        }
        result = users_collection.insert_one(sample_user)
        print(f"✅ Sample user created with ID: {result.inserted_id}")

    # Test inserting a sample task
    if tasks_count == 0:
        print("📝 Creating sample task...")
        sample_task = {
            "username": "testuser",
            "task": "Test task from MongoDB integration",
            "progress": 50,
            "due_date": date.today().isoformat(),
            "created_at": date.today().isoformat()
        }
        result = tasks_collection.insert_one(sample_task)
        print(f"✅ Sample task created with ID: {result.inserted_id}")

    print("🎉 MongoDB integration test completed successfully!")
    print("\n📋 Summary:")
    print(f"   - Database: {DB_NAME}")
    print(f"   - Connection: ✅ Working")
    print(f"   - Users collection: ✅ Accessible")
    print(f"   - Tasks collection: ✅ Accessible")

except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    exit(1)

finally:
    if 'client' in locals():
        client.close()
        print("🔌 Connection closed.")