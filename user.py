import os
import shutil
from filehandlers import getData, writeData, createFile, delete


class User:
    def __init__(self,username:str):
        self.username = username
        return

    def checkExists(self):
        return os.path.exists(f"accounts/{self.username}")
    def readUserFile(self):
        try:
            data = getData(filedir=f"accounts/{self.username}")
        except FileNotFoundError:
            raise FileNotFoundError(f"User file for '{self.username}' not found.")
        else:
            self.password = data.get("password",[None])[0]
            self.accounttype = data.get("accounttype",[None])[0]
            self.priority = int(data.get("priority",[0])[0])
            self.events = data.get("events",[])
    def createUserFile(self,password:str,accounttype:str,priority:str = "0",events:list=[]):
        print(f'Creating user file for {self.username}, with password {password}, account type {accounttype}, priority {priority}, events {events}')
        if self.checkExists():
            raise FileExistsError(f"User file for '{self.username}' already exists.")
        else:
            params = {"password":password,
                      "accounttype":accounttype, 
                      "priority": priority, 
                      "events":events}
            print(params)
            createFile(filedir=f"accounts/{self.username}",params=params)
    
    def login(self,password:str)-> bool:
        try:
            self.readUserFile()
        except FileNotFoundError:
            raise FileNotFoundError(f"User file for '{self.username}' not found.")
        else:
            if self.password == password:
                print(f"User '{self.username}' logged in successfully.")
                return True
            else:
                print(f"Incorrect password for user '{self.username}'.")
                return False
    def register(self,password:str,accounttype:str="student",priority:str = "0",events:list=[]):
        try:
            self.createUserFile(password,accounttype,priority,events)
        except FileExistsError:
            raise FileExistsError(f"User file for '{self.username}' already exists.")
        else:
            print(f"User '{self.username}' registered successfully.")