from flask import Flask
import os
import socket

app = Flask(__name__)

VERSION = os.environ.get('APP_VERSION', '1.0.0')
APP_ENV = os.environ.get('APP_ENV', 'unknown')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'info')
API_KEY = os.environ.get('API_KEY', 'not-set')
POD_NAME = socket.gethostname()

@app.route('/')
def home():
    return f'''
    <html>
        <body style="font-family: Arial; text-align: center; padding: 50px; background-color: #E8F5E9;">
            <h1>Flask on Kubernetes!</h1>
            <h2 style="color: #2E7D32;">Version: {VERSION}</h2>
            <table style="margin: auto; border-collapse: collapse;">
                <tr><td style="padding: 8px; text-align: left;"><strong>Environment:</strong></td><td style="padding: 8px;">{APP_ENV}</td></tr>
                <tr><td style="padding: 8px; text-align: left;"><strong>Log Level:</strong></td><td style="padding: 8px;">{LOG_LEVEL}</td></tr>
                <tr><td style="padding: 8px; text-align: left;"><strong>API Key:</strong></td><td style="padding: 8px;">{API_KEY[:8]}****</td></tr>
                <tr><td style="padding: 8px; text-align: left;"><strong>Pod:</strong></td><td style="padding: 8px;">{POD_NAME}</td></tr>
            </table>
        </body>
    </html>
    '''

@app.route('/health')
def health():
    return {"status": "healthy", "version": VERSION, "env": APP_ENV, "pod": POD_NAME}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
