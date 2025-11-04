import os
from flask import Flask, request, send_file
from dotenv import load_dotenv
from session import Session
import shutil 
from pathlib import Path
import updates
import tempfile

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
        classes = data[2]
        print(f"Read password: {password2} and comparing with {password}")
        if password2 == password:
            if len(password2) < 1 or len(account_type) < 1:
                print("Login failed: Malformed account file")
                return "fail"
            print("Login successful")
            return f"success, {username}, {account_type}, {classes}" 
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
    classes = request.form.get("classes")
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
            file.write(f"{password}\n{accountType}\n{classes}")
            print("Succesfully added new account")
            return "success"
    raise Exception("Something went wrong when creating the account.")

@app.route("/requestSession", methods=["GET"])
def get_sessions_zip():
    base_folder = Path("sessions")
    zip_buf = updates.create_zip_bytes(base_folder, filter_by_date=True)
    if not zip_buf:
        return 'fail'
    return send_file(zip_buf, mimetype='application/zip', as_attachment=True, download_name="sessions_selected.zip")


@app.route("/requestRequests", methods=["GET"])
def set_requests_zip():
    base_folder = Path("requests")
    zip_buf = updates.create_zip_bytes(base_folder, filter_by_date=False)
    if not zip_buf:
        return 'fail'
    return send_file(zip_buf, mimetype='application/zip', as_attachment=True, download_name="requests.zip")

@app.route("/requestSessionEntry", methods = ["POST", "GET"])
def requestSessionEntry():
    print("Received add session request entry")
    key = request.form.get('key')
    username = request.form.get('username')
    acountType = request.form.get("accountType")
    date = request.form.get('date')
    time = request.form.get('time')
    type = request.form.get('type')
    if key != os.getenv("KEY"):
        print("Login failed: Invalid key")
        return "fail"
    
    session = Session(date,time,type)

    print(f"Session:{session.time}:{session.id}")

    if acountType == "student":
        print(f'logged in as student')
        try:
            updates.addToWaitlist(session,username)
        except Exception as e:
            print(f'Error has occured when requesting\n{e}')
            return 'fail'
        else:
            return 'success'
    elif acountType == "teacher":
        print("Logged in as teacher")
        try:
            session.SRChange("session","teacher Supervisor",username,add=True)
        except Exception as e:
            if str(e) == "error1":
                print(f"{username} is already enrolled in the session.")
            elif str(e) == "error2":
                print(f"{username} is already in the waitlist.")
            return 'fail'
        else:
            return 'success'
    else:
        print(f'account error: {acountType}')

        return 'fail'


@app.route("/requestSession", methods = ["POST", "GET"])
def requestSession():

    print("Received add session request")
    key = request.form.get('key')
    username = request.form.get('username')
    accounType = request.form.get("accountType")
    date = request.form.get('date')
    time = request.form.get('time')
    timeEnd= request.form.get('timeEnd')
    teacher = request.form.get('teacher')
    type = request.form.get('type')
    equipment = request.form.get('equipment')
    if key != os.getenv("KEY"):
        print("Login failed: Invalid key")
        return "fail"
    
    session = Session(date,time,type)

    print(f"Session:{session.time}:{session.id}")
    if accounType == "student":
        print(f'logged in as student')
        try:
            session.requestSession(username,timeEnd,teacher,equipment)
        except FileExistsError as e:
            if str(e) == "Session request already made":
                print("Session reqeust already exists, adding user to requestees")
                try:
                    session.SRChange("request","requestees",username,add = True)
                except Exception as e:
                    print("Error:\n", e)
                    return 'fail'
            else:
                if str(e) == "Session file already exists":
                    print("Session already exists, cannot request")
                    return 'fail'            
        except Exception as e:
            print(f'Error has occured when requesting\n{e}')
            return 'fail'
        else:
            ...
            return 'success'
    elif accounType == "teacher":
        print("Logged in as teacher")
        try:
            session.setSession(timeEnd,username,equipment)
        except Exception as e:
            print(f'Error has occured during session request\n{e}')
            return 'fail'
        else: 
            return 'success'
    else:
        print(f'account error: {accounType}')
        return 'fail'

@app.route("/teacher_cancelation", methods = ["POST", "GET"])
def teacher_cancelation():
    print("Received teacher cancelation request")
    key = request.form.get('key')
    username = request.form.get('username')
    accountType = request.form.get("accountType")
    motive = request.form.get('motive')
    date = request.form.get('date')
    time = request.form.get('time')
    type = request.form.get('type')
    if key != os.getenv("KEY"):
        print("Login failed: Invalid key")
        return "fail"
    
    session = Session(date,time,type)

    print(f"Session:{session.time}:{session.id}")

    try:
        session.cancelation(username,accountType)
    except Exception as e:
        print(f'Error has occured during teacher cancelation\n{e}')
        return 'fail'
    else: 
        return 'success'

@app.route("/student_cancelation", methods = ["POST", "GET"])
def student_cancelation():

    try:
        print("Received student cancelation request")
        key = request.form.get('key')
        username = request.form.get('username')
        accountType = request.form.get("accountType")
        date = request.form.get('date')
        time = request.form.get('time')
        type = request.form.get('type')
        if key != os.getenv("KEY"):
            print("Login failed: Invalid key")
            return "fail"
    
        session = Session(date,time,type)

        print(f"Session:{session.time}:{session.id}")
    except Exception as e:
        print(f'Error accessing session for cancelation\n{e}')
        return 'fail'

    try:
        session.cancelation(username,accountType)
    except Exception as e:
        print(f'Error has occured during student cancelation\n{e}')
        return 'fail'
    else: 
        return 'success'
    
    
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=os.getenv("PORT", 5000)) 
