from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
from pymongo import MongoClient
from pymongo.errors import PyMongoError 

app = Flask(__name__)


MONGO_URI = "mongodb+srv://<your_username>:<your_password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
try:
    client = MongoClient(MONGO_URI)
    db = client.flask_db
    items_collection = db.items 
    print("Successfully connected to MongoDB Atlas!")
except PyMongoError as e:
    print(f"Error connecting to MongoDB Atlas: {e}")
    client = None 


@app.route('/api/items', methods=['GET'])
def get_items():
   
    try:
        with open('data.json', 'r') as f: 
            data = json.load(f) 
        return jsonify(data) 
    except FileNotFoundError:
        return jsonify({"error": "data.json not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON from data.json"}), 500

@app.route('/')
def index():
   
    return render_template('index.html') 

@app.route('/submit', methods=['POST'])
def submit_data():
  
    if not client: 
        return render_template('index.html', error="Database connection error. Please try again later."), 500 

    item_name = request.form.get('item_name')
    item_description = request.form.get('item_description')

    if not item_name or not item_description:
        return render_template('index.html', error="Both Item Name and Item Description are required."), 400 

    try:
        new_item = {
            "name": item_name,
            "description": item_description
        }
        items_collection.insert_one(new_item) 
        return redirect(url_for('success_page'))  
    except PyMongoError as e:
        return render_template('index.html', error=f"Database submission error: {e}"), 500 
    except Exception as e:
        return render_template('index.html', error=f"An unexpected error occurred: {e}"), 500 

@app.route('/success')
def success_page():
  
    return render_template('success.html') 

if __name__ == '__main__':
    app.run(debug=True)
