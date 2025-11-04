import os
import shutil
from filehandlers import getData, writeData


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
    def createUserFile(self,password:str,accounttype:str,priority:int=0,events:list=[]):
        if self.checkExists():
            raise FileExistsError(f"User file for '{self.username}' already exists.")
        else:
            writeData(filedir=f"accounts/{self.username}",dataType="password",data=password)
            writeData(filedir=f"accounts/{self.username}",dataType="accounttype",data=accounttype)
            writeData(filedir=f"accounts/{self.username}",dataType="priority",data=str(priority))
            writeData(filedir=f"accounts/{self.username}",dataType="events",data=",".join(events))
    