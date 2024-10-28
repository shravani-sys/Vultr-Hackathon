from flask import Flask, request, jsonify, render_template
from transformers import pipeline
from vosk import Model, KaldiRecognizer
import wave
import os
import json
import sqlite3
from datetime import datetime
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# Load the Vosk model for speech-to-text
model_path = "models/vosk-model-small-en-us-0.15"

model = Model(model_path)

# Load the pre-trained sentiment analysis model
sentiment_analysis = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Initialize SQLite database
conn = sqlite3.connect('interactions.db', check_same_thread=False)
cursor = conn.cursor()

# Create table for storing interaction data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT,
        text TEXT,
        emotion TEXT,
        timestamp TEXT
    )
''')
conn.commit()

# Function to transcribe speech using Vosk
def transcribe_audio(audio_file):
    wf = wave.open(audio_file, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        return {"error": "Audio file must be WAV format mono PCM with a 16kHz sample rate"}

    rec = KaldiRecognizer(model, wf.getframerate())

    transcript = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            transcript += result.get("text", "") + " "

    result = json.loads(rec.FinalResult())
    transcript += result.get("text", "")

    return transcript.strip()

# Function to store interactions in the database
def store_interaction(customer_id, text, emotion):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO interactions (customer_id, text, emotion, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (customer_id, text, emotion, timestamp))
    conn.commit()

# Route for sentiment analysis on text
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")
    customer_id = data.get("customer_id", "anonymous")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = sentiment_analysis(text)
    emotion = result[0]['label']

    store_interaction(customer_id, text, emotion)

    return jsonify({"sentiment": result})

# Route for speech-to-text and sentiment analysis
@app.route("/analyze-voice", methods=["POST"])
def analyze_voice():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    customer_id = request.form.get("customer_id", "anonymous")

    audio_path = "/tmp/temp_audio.wav"
    audio_file.save(audio_path)

    transcript = transcribe_audio(audio_path)
    if not transcript:
        return jsonify({"error": "Could not transcribe audio"}), 500

    sentiment_result = sentiment_analysis(transcript)
    emotion = sentiment_result[0]['label']

    store_interaction(customer_id, transcript, emotion)

    return jsonify({"transcript": transcript, "sentiment": sentiment_result})

# Route to display the Admin Dashboard with filtering
@app.route("/dashboard", methods=["GET"])
def dashboard():
    customer_id = request.args.get('customer_id', '')
    start_date = request.args.get('start_date', '2000-01-01')
    end_date = request.args.get('end_date', datetime.now().strftime("%Y-%m-%d"))

    query = "SELECT * FROM interactions WHERE timestamp BETWEEN ? AND ?"
    params = [start_date, end_date]

    if customer_id:
        query += " AND customer_id = ?"
        params.append(customer_id)

    cursor.execute(query, params)
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=['id', 'customer_id', 'text', 'emotion', 'timestamp'])

    sentiment_trend = df.groupby(['timestamp', 'emotion']).size().reset_index(name='count')

    fig = px.line(sentiment_trend, x='timestamp', y='count', color='emotion',
                  title='Customer Sentiment Over Time')

    plot_div = fig.to_html(full_html=False)

    return render_template('dashboard.html', plot_div=plot_div, data=df.to_dict('records'))

# API route to serve the latest interaction data for real-time updates
@app.route("/api/interaction-data", methods=["GET"])
def get_interaction_data():
    cursor.execute("SELECT * FROM interactions")
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=['id', 'customer_id', 'text', 'emotion', 'timestamp'])

    sentiment_trend = df.groupby(['timestamp', 'emotion']).size().reset_index(name='count')

    sentiment_trend_json = sentiment_trend.to_json(orient='records')
    interactions_json = df.to_json(orient='records')

    return jsonify({
        "sentiment_trend": json.loads(sentiment_trend_json),
        "interactions": json.loads(interactions_json)
    })

# Route for recommendation based on interaction history
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    customer_id = data.get("customer_id", "anonymous")

    cursor.execute("SELECT emotion FROM interactions WHERE customer_id = ? ORDER BY timestamp DESC LIMIT 1", (customer_id,))
    last_emotion = cursor.fetchone()[0]

    if last_emotion == 'NEGATIVE':
        recommendation = "We noticed you had a frustrating experience. How about trying our premium support?"
    else:
        recommendation = "Thank you for your positive feedback! Check out our new features."

    return jsonify({"recommendation": recommendation})

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
