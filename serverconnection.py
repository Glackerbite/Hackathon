import os
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.getenv('KEY', 'BASELINEKEY')
print("Secret Key:", app.config['SECRET_KEY'])
print("Port:", os.getenv('PORT'))

@app.route('/')
def index():
    print("Received a request from:", request.remote_addr)
    return "Server is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT')))