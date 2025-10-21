import os

class Session:
    def __init__(self, date:str, time:str, place:str):
        self.date = date
        self.time = time #ddmmyy
        self.place = place #physics, biology, chemistry
        self.id = None
        
        self.setId()
        
    def setId(self):
        if self.id == None:
            if self.place == "physics" or self.place == " chemistry":
                self.id = f'm{self.time}'
            elif self.place == "biology":
                self.id = f'b{self.time}'
            else:
                raise Exception("ERROR IN FUNC:setId")
    
    def filecheck(self)-> bool:
        return os.path.exists(f'sessions/{self.date}/{self.id}')
    
    def checkDateFile(self):
        if not os.path.exists(f'sessions/{self.date}'):
            print(f"Added date folder for session of {self.date}")
            os.makedirs(f'sessions/{self.date}')

    def setSession(self):
        if not self.filecheck():
            self.checkDateFile()
            ...
            
    
    def requestSession(self):
        ...
    def delete(self,type:str):
        """
        Either deletes the session file or folder
        """
        if type == "folder":
            try:
                os.rmdir(f"sessions/{self.date}")
            except FileNotFoundError:
                print(f"sessions/{self.date} Folder was not cound")
            except OSError as e:
                print("Error not all session deleted")
        elif type == "file":
            try:
                os.remove(f'sessions/{self.date}/{self.id}')
            except FileExistsError:
                print(f"Error: sessions/{self.date}/{self.id} doesnt exist.")
        else:
            raise Exception("if ERROR in delete")


    def sessionDataChange(self):
        ...
    
    def __str__(self):
        ...   