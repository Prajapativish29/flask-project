from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
from pymongo import MongoClient
from pymongo.errors import PyMongoError # Import specific MongoDB error

app = Flask(__name__)

# MongoDB Atlas Connection
# Replace with your actual MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://prajapativish29:17101QXCFXeaNmAJ@flask-app.ydoa1hf.mongodb.net/?retryWrites=true&w=majority&appName=flask-app"
try:
    client = MongoClient(MONGO_URI)
    db = client.flask_db # Choose a database name
    items_collection = db.items # Choose a collection name
    print("Successfully connected to MongoDB Atlas!")
except PyMongoError as e:
    print(f"Error connecting to MongoDB Atlas: {e}")
    client = None # Set client to None if connection fails to prevent further errors


@app.route('/api/items', methods=['GET'])
def get_items():
    """
    Reads data from data.json and returns it as a JSON list.
    """
    try:
        with open('data.json', 'r') as f: # 
            data = json.load(f) # 
        return jsonify(data) # 
    except FileNotFoundError:
        return jsonify({"error": "data.json not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON from data.json"}), 500

@app.route('/')
def index():
    """
    Renders the form page.
    """
    return render_template('index.html') # 

@app.route('/submit', methods=['POST'])
def submit_data():
    """
    Handles form submission, inserts data into MongoDB Atlas,
    and redirects on success or displays error on failure.
    """
    if not client: # Check if MongoDB client was initialized successfully
        return render_template('index.html', error="Database connection error. Please try again later."), 500 # 

    item_name = request.form.get('item_name')
    item_description = request.form.get('item_description')

    if not item_name or not item_description:
        return render_template('index.html', error="Both Item Name and Item Description are required."), 400 # 

    try:
        new_item = {
            "name": item_name,
            "description": item_description
        }
        items_collection.insert_one(new_item) # 
        return redirect(url_for('success_page')) # 
    except PyMongoError as e:
        return render_template('index.html', error=f"Database submission error: {e}"), 500 # 
    except Exception as e:
        return render_template('index.html', error=f"An unexpected error occurred: {e}"), 500 # 

@app.route('/success')
def success_page():
    """
    Renders the success message page.
    """
    return render_template('success.html') # 

if __name__ == '__main__':
    app.run(debug=True)