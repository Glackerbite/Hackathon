import os
from flask import Flask, request, jsonify
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
    print("Received login request")
    key = request.form.get('key')
    username = request.form.get('username')
    password = request.form.get('password')
    print(f"Username: {username}, Password: {password}")
    if key != "OKAYTHISISTHEKEY":
        print("Login failed: Invalid key")
        return "fail"
    try:
        userfile= open("accounts/"+username+".txt" , 'r') 
    except FileNotFoundError:
        print("Login failed: User not found")
        return "fail"
    except Exception as e:
        print("Error accessing account file:", e)
        return "fail"
    else:
        data= userfile.read()
        data = data.splitlines()
        password2 = data[0]

        userfile.close()

        print(f"Read password: {password2} and comparing with {password}")
        if password2 == password:
            if len(data) > 1:
                account_type = data[1]
            else:
                print("Login failed: Malformed account file")
                return "fail"
            print("Login successful")
            return f"success, {account_type}" 
        print("Login failed: Incorrect password")
        userfile.close()
        return "fail"
        


if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000) 

