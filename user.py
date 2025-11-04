import os
from pathlib import Path

class User:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.accountType = ""
        self.priority = False

    def loadFromFile(self,username:str):
        userPath = Path(f"accounts/{username}.txt")
        if not userPath.exists():
            raise FileNotFoundError("User does not exist")
        with open(userPath,"r") as file:
            lines = file.readlines()
            self.username = username
            self.password = lines[0].strip()
            self.accountType = lines[1].strip()
            if len(lines) > 2 and lines[2].strip() == "priority":
                self.priority = True