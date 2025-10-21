import os
from flask import Flask, request
from dotenv import load_dotenv
from session import Session
load_dotenv()
app = Flask(__name__)
app.config['DEBUG'] = True
print("Port:", os.getenv('PORT'))

@app.route('/login', methods=['POST','GET'])
def login():
    print("Received login request")
    key = request.form.get('key')
    username = request.form.get('username')
    password = request.form.get('password')
    print(f"Username: {username}, Password: {password}")
    if key != os.getenv("KEY"):
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
        userfile.close()
        
        password2 = data[0]
        account_type = data[1]
        print(f"Read password: {password2} and comparing with {password}")
        if password2 == password:
            if len(password2) < 1 or len(account_type) < 1:
                print("Login failed: Malformed account file")
                return "fail"
            print("Login successful")
            return f"success, {username}, {account_type}" 
        print("Login failed: Incorrect password")
        userfile.close()
        return "fail"
@app .route('/register', methods=['POST'])
def register():
    print("Received registration request")
    key = request.form.get('key')
    username = request.form.get('username')
    password = request.form.get('password')
    accountType = "student"
    if key != os.getenv("KEY"):
        print("Login failed: Invalid key")
        return "fail"
    
    if len(password) < 1:
        print(f'Missing password')
        return "fail"
    
    print(f"Attempting to register {accountType}{username} with password {password}.")

    if os.path.exists(f"accounts/{username}.txt"):
        print(f"{username} already exists")
        return 'fail'
    else:
        with open(f"accounts/{username}.txt","w") as file:
            file.write(f"{password}\n{accountType}")
            print("Succesfully added new account")
            return "success"
    raise Exception("Something went wrong when creating the account.")

@app.route('/calendar', methods=['POST'])
def calendar():
    
    
    return ...

@app.route("/requestSession", methods = ["POST", "GET"])
def requestSession():

    print("Received add session request")
    key = request.form.get('key')
    username = request.form.get('username')
    accounType = request.form.get("accountType")
    date = request.form.get('date')
    time = request.form.get('time')
    lab = request.form.get('lab')
    equipment = request.form.get('equipment')
    

    if key != os.getenv("KEY"):
        print("Login failed: Invalid key")
        return "fail"
    


    return 


if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=os.getenv("PORT", 5000)) 