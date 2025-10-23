import os

class Session:
    def __init__(self, date:str, time:str, type:str):
        self.date = date #ddmmyy 
        self.time = time #hhmm
        self.type = type #physics, biology, chemistry
        self.id = None
        
        self.setId()
        
    def setId(self):
        if self.id == None:
            if self.type == "physics" or self.type == "chemistry" or self.type == "chemistry and physics":
                self.id = f'M{self.time}'
            elif self.type == "biology":
                self.id = f'B{self.time}'
            else:
                print("Error in function setId: Type syntax error.")
        else:
            print("ID already set")
            
     
    def filecheck(self)-> bool:
        return os.path.exists(f'sessions/{self.date}/{self.id}')
    
    def checkDateFile(self):
        if not os.path.exists(f'sessions/{self.date}'):
            print(f"Added date folder for session of {self.date}")
            os.makedirs(f'sessions/{self.date}')

    def setSession(self, timeEnd:str, teacher:str,equipment:str, places=10, priorityPlaces=3):
        
        if not self.filecheck():
            self.checkDateFile()
            try:    
                with open(f'sessions/{self.date}/{self.id}','w') as f:
                    f.write(f'time end:{timeEnd}\nsession type:{self.type}\nteacher Supervisor:{teacher}\nequipment:{equipment}\nplaces:{places}\nstudents:\nwaitlist:')
            except Exception as e:
                print(f'Error adding session: {e}')
            else:
                print(f"Session added succesfully with: {self.id}, time end:{timeEnd}\nsessions type:{self.type}\nteacher Supervisor:{teacher}\nequipment:{equipment}\nplaces:{places}")
        else:
            print(f'Error session on {self.date}, of {self.type} at {self.time} already exists')
                 

    def requestSession(self,user:str,timeEnd:str,teacherRequested:str,equipment=""):
        if not self.filecheck() and not os.path.exists(f'sessionRequests/{self.date}{self.id}'):
            print("Creating request.")
            nl = "\n"
            try:
                with open(f'sessionRequests/{self.date}{self.id}','w') as f:
                    f.write(f'resquestees:{user}\ntime end:{timeEnd}\nsessions type:{self.type}\nteacher Supervisor:{teacherRequested}\nequipment:{equipment}')

            except Exception as e: 
                print(f"Error has occured in request session: \n{e}")
            else:
                print("Session request sucessfully made.")
    def delete(self,fileType="",type="session"):
        """
        Handles file and folder deletion 
        """
        sessionDirectory = f'sessions/{self.date}'
        requestDirectory = f'sessionRequests/{self.date}{self.id}'
        if type == "session":
            if fileType == "folder":
                try:
                    os.rmdir(sessionDirectory)
                except FileNotFoundError:
                    print(f"{sessionDirectory} Folder was not cound")
                except OSError:
                    print("Error not all session in folder deleted")
                except Exception as e:
                    print(f'Error in delete function:\n {e} ')
            elif fileType == "file":
                try:
                    os.remove(f'{sessionDirectory}/{self.id}')
                except FileExistsError:
                    print(f"Error: {sessionDirectory}/{self.id} doesnt exist.")
                except Exception as e:
                    print(f'Error in delete function:\n {e} ')
            else:
                raise Exception("ERROR in delete: fileType syntax error.")
        elif type == "request":
            try:
                os.remove(requestDirectory)
            except FileNotFoundError:
                print(f"{requestDirectory} request not found.")
            except Exception as e:
                print(f'Error in delete function:\n {e} ')
            

    def s_or_r_DataChange(self,type:str,dataType:str,data:str):
        ...
    
    def __str__(self):
        return f'date:{self.date}, time:{self.time}, id:{self.id}' 
      