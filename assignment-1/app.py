from flask import Flask, jsonify
import json

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)


   
