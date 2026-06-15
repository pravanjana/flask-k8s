from flask import Flask
import os
import socket

app = Flask(__name__)

VERSION = os.environ.get('APP_VERSION', '2.0.0')
POD_NAME = socket.gethostname()

@app.route('/')
def home():
    return f'''
    <html>
        <body style="font-family: Arial; text-align: center; padding: 50px; background-color: #E3F2FD;">
            <h1>Flask on Kubernetes!</h1>
            <h2 style="color: #1565C0;">Version: {VERSION} — Updated!</h2>
            <p>Pod name: <strong>{POD_NAME}</strong></p>
            <p>Deployed via Jenkins + GKE</p>
            <p>Rolling update — zero downtime!</p>
        </body>
    </html>
    '''

@app.route('/health')
def health():
    return {"status": "healthy", "version": VERSION, "pod": POD_NAME}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
