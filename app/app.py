from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client.task_manager # Your database name
tasks_collection = db.tasks # Your collection name

@app.route('/')
def home():
    return "Task Manager API is running on python version!"

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        task_data = request.json
        if not task_data:
            return jsonify({"error": "No data provided"}), 400

        # Validate required fields (you can add more comprehensive validation)
        required_fields = ['title', 'assignedTo', 'status', 'priority', 'startDate', 'endDate']
        if not all(field in task_data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Convert date strings to datetime objects for better storage/querying
        try:
            task_data['startDate'] = datetime.strptime(task_data['startDate'], '%d%b%Y')
            task_data['endDate'] = datetime.strptime(task_data['endDate'], '%d%b%Y')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use DDMonYYYY (e.g., 15Jun2025)"}), 400

        # Ensure 'id' is unique or use MongoDB's default _id
        # For simplicity, we'll use the provided 'id' as a unique identifier if present,
        # otherwise MongoDB's _id will be generated.
        # If 'id' is meant to be a primary key, you might want to check for its existence
        # before insertion or use it as _id if it's guaranteed unique and immutable.
        # Here, we'll store it as a regular field.

        result = tasks_collection.insert_one(task_data)
        task_data['_id'] = str(result.inserted_id) # Convert ObjectId to string for JSON response
        return jsonify({"message": "Task created successfully", "task": task_data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = []
        for task in tasks_collection.find():
            task['_id'] = str(task['_id']) # Convert ObjectId to string
            # Convert datetime objects back to string for consistent output if needed
            task['startDate'] = task['startDate'].strftime('%d%b%Y')
            task['endDate'] = task['endDate'].strftime('%d%b%Y')
            tasks.append(task)
        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    try:
        # Assuming 'id' field is used for lookup, not _id
        task = tasks_collection.find_one({"_id": ObjectId(task_id)})
        if task:
            task['_id'] = str(task['_id'])
            task['startDate'] = task['startDate'].strftime('%d%b%Y')
            task['endDate'] = task['endDate'].strftime('%d%b%Y')
            return jsonify(task), 200
        return jsonify({"message": "Task not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/<task_id>', methods=['PUT'])
def edit_task(task_id):
    try:
        # Parse the request body for updated task data
        updated_data = request.json

        # Convert 'startDate' and 'endDate' to datetime objects if they are provided
        if 'startDate' in updated_data:
            try:
                updated_data['startDate'] = datetime.strptime(updated_data['startDate'], '%d%b%Y')
            except ValueError:
                return jsonify({"error": "Invalid startDate format. Use DDMonYYYY (e.g., 15Jun2025)"}), 400

        if 'endDate' in updated_data:
            try:
                updated_data['endDate'] = datetime.strptime(updated_data['endDate'], '%d%b%Y')
            except ValueError:
                return jsonify({"error": "Invalid endDate format. Use DDMonYYYY (e.g., 15Jun2025)"}), 400

        # Update the task in the database
        result = tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": updated_data})
        if result.matched_count > 0:
            return jsonify({"message": "Task updated successfully"}), 200
        return jsonify({"message": "Task not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        # Delete the task from the database
        result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
        if result.deleted_count > 0:
            return jsonify({"message": "Task deleted successfully"}), 200
        return jsonify({"message": "Task not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)