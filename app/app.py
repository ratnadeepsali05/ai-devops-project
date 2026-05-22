from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def home():
    return "AI DevOps Monitoring Project Running Successfully"

@app.route('/health')
def health():
    return {
        "status": "healthy"
    }

@app.route('/error')
def error():
    errors = [
        "Database Connection Timeout",
        "Memory Overflow Detected",
        "Application Crash",
        "High CPU Usage"
    ]

    return {
        "error": random.choice(errors)
    }, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)