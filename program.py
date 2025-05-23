from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

db_config = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', 'plant_db'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as e:
        print("Connection error:", e)
        return None

@app.route('/api/plants', methods=['GET'])
def get_all_plants():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM plants")
    plants = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(plants)

@app.route('/api/plants/<int:id>', methods=['GET'])
def get_plant(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM plants WHERE id = %s", (id,))
    plant = cursor.fetchone()
    cursor.close()
    conn.close()
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    return jsonify(plant)

@app.route('/api/plants', methods=['POST'])
def add_plant():
    data = request.json
    required = ['name', 'species', 'water_frequency']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO plants (name, species, last_watered, water_frequency, sunlight_requirements, photo_url)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data['name'],
        data['species'],
        data.get('last_watered', None),
        data['water_frequency'],
        data.get('sunlight_requirements', ''),
        data.get('photo_url', '')
    ))
    conn.commit()
    plant_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({**data, 'id': plant_id}), 201

@app.route('/api/plants/<int:id>', methods=['PUT'])
def update_plant(id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    fields = []
    values = []
    for field in ['name', 'species', 'last_watered', 'water_frequency', 'sunlight_requirements', 'photo_url']:
        if field in data:
            fields.append(f"{field} = %s")
            values.append(data[field])

    if not fields:
        return jsonify({'error': 'No valid fields to update'}), 400

    values.append(id)
    query = f"UPDATE plants SET {', '.join(fields)} WHERE id = %s"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, tuple(values))
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Plant not found'}), 404

    cursor.close()
    conn.close()
    return jsonify({'message': 'Plant updated successfully'})

@app.route('/api/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM plants WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({'error': 'Plant not found'}), 404
    return jsonify({'message': 'Plant deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)