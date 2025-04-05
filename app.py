from flask import Flask, request, jsonify, render_template, url_for
from twilio.rest import Client
import geopy.distance
import sqlite3
import os

app = Flask(_name_)

# Twilio Configuration
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"
ADMIN_PHONE_NUMBER = "your_phone_number"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT, phone TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS emergency_contacts (user TEXT, contact_name TEXT, contact_phone TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data.get("name").lower()
    password = data.get("password")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name = ? AND password = ?", (name, password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"status": "success", "message": "Login successful"})
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials or restricted access"})

@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    name = data.get("name")
    message = f"{name} triggered an Emergency Alert! Live Location: https://maps.google.com/?q={latitude},{longitude}"

    client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=ADMIN_PHONE_NUMBER)
    return jsonify({"status": "success", "message": "Alert sent successfully!"})

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    phone = data.get("phone")
    name = data.get("name")
    message = f"{name} needs your help urgently! This is an emergency."

    client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=phone)
    return jsonify({"status": "success", "message": "Message sent successfully!"})

@app.route('/add_contacts', methods=['POST'])
def add_contacts():
    data = request.json
    user = data.get("user")
    contacts = data.get("contacts")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    for contact in contacts:
        c.execute("INSERT INTO emergency_contacts (user, contact_name, contact_phone) VALUES (?, ?, ?)",
                  (user, contact["name"], contact["phone"]))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Contacts added successfully!"})

@app.route('/safe_routes', methods=['POST'])
def safe_routes():
    data = request.json
    start = data.get("start")
    destination = data.get("destination")

    # This is a static mock response. You can later integrate Google Maps API for real route safety analysis.
    safe_routes_list = [
        {"route": "Route 1", "distance": "2.5 km", "safety_level": "High"},
        {"route": "Route 2", "distance": "3.0 km", "safety_level": "Medium"},
        {"route": "Route 3", "distance": "3.5 km", "safety_level": "Low"}
    ]

    return jsonify({"status": "success", "routes": safe_routes_list})

if _name_ == '_main_':
    if not os.path.exists("users.db"):
        init_db()
    app.run(debug=True)
