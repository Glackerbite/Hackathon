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

@app.route('/calendar', methods=['POST'])
def calendar():
    data = request.get_json(silent=True)
    if data is None:
        return {"error": "invalid or missing JSON"}, 400
    print("Calendar data received:", data)
    return {"status": "Calendar data received"}, 200

@app.route('/login', methods=['POST','GET'])
def login():
    # Accept JSON body for POST; for GET show a simple message
    if request.method == 'GET':
        return {"status": "Send a POST with JSON {username, password}"}, 200

    data = request.get_json(silent=True)
    if not data:
        return {"error": "Missing JSON body"}, 400

    print("Receive login request")
    username = data.get('username')
    password = data.get('password')
    print(f"Username: {username}, Password: {password}")

    if not username:
        return {"error": "username is required"}, 400

    # Build a safe path to the account file
    account_path = os.path.join(os.path.dirname(__file__), 'accounts', f"{username}.txt")
    try:
        with open(account_path, 'r') as f:
            account_data = f.read()
            print("Account file contents (truncated):", account_data[:200])
    except FileNotFoundError:
        return {"error": "Account does not exist"}, 404
    except Exception as e:
        print("Error accessing account file:", e)
        return {"error": "Internal server error"}, 500

    # TODO: verify password against stored value (not implemented)
    return {"status": "login checked (not authenticated)"}, 200
if __name__ == '__main__':
    # Provide a safe default port when PORT is not set
    port = int(os.getenv('PORT', '5000'))
    app.run(host='0.0.0.0', port=port)

