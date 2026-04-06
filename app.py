from flask import Flask, render_template, request, redirect, session
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import date, datetime
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.secret_key = os.getenv('SECRET_KEY', 'secret123')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection with error handling
try:
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://giridhards18_db_user:uAovwnOOK26qYUJo@taskpilot.xqvmkpd.mongodb.net/')
    DB_NAME = os.getenv('MONGODB_DB_NAME', 'taskpilot')
    
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000, connectTimeoutMS=10000)
    db = client[DB_NAME]
    
    # Test connection
    db.command('ping')
    logger.info('MongoDB connected successfully')
    
    # Collections
    users_collection = db.users
    tasks_collection = db.tasks
    
    # Ensure indexes for better performance
    users_collection.create_index("username", unique=True)
    tasks_collection.create_index("username")
    tasks_collection.create_index("due_date")
    logger.info('Database indexes created')
    
except Exception as e:
    logger.error(f'MongoDB Connection Error: {e}')
    users_collection = None
    tasks_collection = None
    db = None

@app.context_processor
def inject_globals():
    """Inject global variables into all templates"""
    return {
        'now': datetime.now(),
        'today': date.today(),
        'date': date,
        'datetime': datetime
    }


# HOME
@app.route('/', methods=['GET', 'POST'])
def home():
    if "username" not in session:
        return redirect('/login')

    try:
        if tasks_collection is None:
            return "Database connection error. Please try again later."

        if request.method == "POST":
            task = request.form.get("task")
            try:
                progress = int(request.form.get("progress") or 0)
            except ValueError:
                progress = 0
            due_date = request.form.get("due_date")

            # Insert new task
            task_doc = {
                "username": session["username"],
                "task": task,
                "progress": progress,
                "due_date": due_date,
                "created_at": date.today().isoformat()
            }
            tasks_collection.insert_one(task_doc)

        # Get all tasks for the user
        tasks_cursor = tasks_collection.find({"username": session["username"]})
        tasks = list(tasks_cursor)

        # Convert ObjectId to string for template compatibility
        for task in tasks:
            task["_id"] = str(task["_id"])

        total = len(tasks)
        percent = int(sum([t["progress"] for t in tasks]) / total) if total > 0 else 0

        return render_template("index.html", tasks=tasks, username=session["username"], percent=percent)
    
    except Exception as e:
        logger.error(f"Home route error: {e}")
        return f"Error: {str(e)}", 500


# COMPLETE
@app.route('/complete/<task_id>')
def complete(task_id):
    if tasks_collection is None:
        return "Database connection error", 500
    
    try:
        # Update task progress to 100
        tasks_collection.update_one(
            {"_id": ObjectId(task_id), "username": session.get("username")},
            {"$set": {"progress": 100}}
        )
    except Exception as e:
        logger.error(f"Complete task error: {e}")
        pass  # Invalid ObjectId, just redirect

    return redirect('/')


# DELETE
@app.route('/delete/<task_id>')
def delete(task_id):
    if tasks_collection is None:
        return "Database connection error", 500
    
    try:
        # Delete the task
        tasks_collection.delete_one(
            {"_id": ObjectId(task_id), "username": session.get("username")}
        )
    except Exception as e:
        logger.error(f"Delete task error: {e}")
        pass  # Invalid ObjectId, just redirect

    return redirect('/')


# EDIT
@app.route('/edit/<task_id>', methods=['GET', 'POST'])
def edit(task_id):
    if tasks_collection is None:
        return "Database connection error", 500
    
    try:
        task = tasks_collection.find_one(
            {"_id": ObjectId(task_id), "username": session.get("username")}
        )
    except Exception as e:
        logger.error(f"Edit task error: {e}")
        return redirect('/')  # Invalid ObjectId

    if not task:
        return redirect('/')

    if request.method == "POST":
        new_task = request.form.get("task")
        try:
            progress = int(request.form.get("progress") or 0)
        except ValueError:
            progress = 0
        due_date = request.form.get("due_date")

        # Update the task
        tasks_collection.update_one(
            {"_id": ObjectId(task_id), "username": session.get("username")},
            {"$set": {
                "task": new_task,
                "progress": progress,
                "due_date": due_date
            }}
        )

        return redirect('/')

    # Convert ObjectId to string for template
    task["_id"] = str(task["_id"])
    return render_template("edit.html", task=task)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            if users_collection is None:
                return "Database connection error. Please try again later."
            # Try to insert new user
            user_doc = {
                "username": username,
                "password": password,  # In production, hash the password!
                "created_at": date.today().isoformat()
            }
            users_collection.insert_one(user_doc)
            return redirect('/login')
        except Exception as e:
            # Username already exists (unique index violation)
            logger.error(f"Registration error: {e}")
            if "duplicate key" in str(e).lower():
                return "Username already exists"
            return f"Error: {str(e)}"

    return render_template("register.html")


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            if users_collection is None:
                return "Database connection error. Please try again later."
            
            # Find user with matching credentials
            user = users_collection.find_one({
                "username": username,
                "password": password
            })

            if user:
                session["username"] = username
                return redirect('/')
            else:
                return "Invalid credentials"
        except Exception as e:
            logger.error(f"Login error: {e}")
            return f"Error: {str(e)}"

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)