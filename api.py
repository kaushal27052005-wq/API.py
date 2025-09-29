from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory user storage
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 30},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "age": 25}
]

next_id = 3

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({"success": True, "data": users}), 200

# GET user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify({"success": True, "data": user}), 200
    return jsonify({"success": False, "error": "User not found"}), 404

# POST - Create new user
@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"success": False, "error": "Name and email required"}), 400
    
    new_user = {
        "id": next_id,
        "name": data['name'],
        "email": data['email'],
        "age": data.get('age', None)
    }
    
    users.append(new_user)
    next_id += 1
    
    return jsonify({"success": True, "data": new_user}), 201

# PUT - Update user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
    
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])
    user['age'] = data.get('age', user['age'])
    
    return jsonify({"success": True, "data": user}), 200

# DELETE user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    
    users = [u for u in users if u['id'] != user_id]
    return jsonify({"success": True, "message": "User deleted"}), 200

if __name__ == '__main__':
    print("\nFlask REST API Server")
    print("Running on http://127.0.0.1:5000")
    print("Press CTRL+C to stop\n")
    app.run(debug=True, port=5000)