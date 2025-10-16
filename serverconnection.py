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
    
    
    return ...

@app.route('/login', methods=['POST','GET'])
def login():
    # Accept JSON body for POST; for GET show a simple message
    if request.method == 'POST':
        return {"status": "Send a POST with JSON {username, password}"}, 200

    print("Receive login request")
    request.form.get('username')
    username = request.form.get('username')
    password = request.form.get('password')
    print(f"Username: {username}, Password: {password}")
    try:
        userfile= open("account/"+username+".txt" , 'r') 
    except FileNotFoundError:
        return {"Incorrect username or password"}, 401
    except Exception as e:
        print("Error accessing account file:", e)
        return {"error": "Internal server error"}, 500
    else:
        password2= userfile.read()
        print(f"Read password: {password2} and comparing with {password}")
        if password2 == password:
            userfile.close()
            return {"status": "login successful"}, 200
        userfile.close()
        return {"Incorrect username or password"}, 401
        
    

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000) #

