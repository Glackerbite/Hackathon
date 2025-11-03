import os
import shutil

class Session:
    def __init__(self, date:str, time:str, type:str):
        self.date = date #ddmmyy 
        self.time = time #hhmm
        self.type = type #physics, biology, chemistry
        self.id = None
        
        self.setId()
        
    def setId(self):
        if self.id == None:
            if self.type in ["physics", "chemistry", "chemistry and physics"]:
                self.id = f'M{self.time}'
            elif self.type == "biology":
                self.id = f'B{self.time}'
            else:
                print("Error in function setId: Type syntax error.")
        else:
            print("ID already set")
            
        os.makedirs("sessionRequests", exist_ok=True)
        os.makedirs("sessions",exist_ok=True)
     
    def filecheck(self)-> bool:
        return os.path.exists(f'sessions/{self.date}/{self.id}')
    def reqcheck(self) -> bool:
        return os.path.exists(f'sessionRequests/{self.date}{self.id}')

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
                print(f"Session added succesfully with: {self.id}, time end:{timeEnd}\nsessions type:{self.type}\nteacher Supervisor:{teacher}\nequipment:{equipment}\nplaces:{places}\n")
        else:
            print(f'Error session on {self.date}, of {self.type} at {self.time} already exists')
                 

    def requestSession(self,user:str,timeEnd:str,teacherRequested:str,equipment=""):
        if not self.filecheck() and not self.reqcheck():
            print("Creating request.")
            nl = "\n"
            try:
                with open(f'sessionRequests/{self.date}{self.id}','w') as f:
                    f.write(f'requestees:{user}\ntime end:{timeEnd}\nsession type:{self.type}\nteacher Supervisor:{teacherRequested}\nequipment:{equipment}')

            except Exception as e: 
                print(f"Error has occured in request session: \n{e}")
            else:
                print("Session request sucessfully made.")
        else:
            print(f'Session request already made or session already exists.')
            ...
    def delete(self,fileType="",type="session"):
        """
        Handles file and folder deletion\n
        params:\n
        fileType: ONLY for sessions, use either folder or file \n
        type: default = session, can change to request
        """
        sessionDirectory = f'sessions/{self.date}'
        requestDirectory = f'sessionRequests/{self.date}{self.id}'
        if type == "session":
            if fileType == "folder":
                try:
                    shutil.rmtree(sessionDirectory)
                except FileNotFoundError:
                    print(f"{sessionDirectory} Folder was not found")

                except Exception as e:
                    print(f'Error in delete function:\n {e} ')
            elif fileType == "file":
                try:
                    os.remove(f'{sessionDirectory}/{self.id}')
                except FileNotFoundError:
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
            
    def requestTransfer(self,places=10,priorityPlaces=3):
        if self.filecheck():
            print("Session file already exists, removing request file.")
            self.delete(type="request")
        else:

            with open(f'sessionRequests/{self.date}{self.id}','r') as req, open(f'sessions/{self.date}/{self.id}', "w") as ses:
                # removes the unecesary requestees part and adds the requestees as people in the waitlist
                requestees = req.readline().strip()
                if requestees.startswith("requestees:"):
                    print("R1")
                    requestees = requestees.replace("requestees:", "", 1).strip()
                else:
                    print("error in RequestTransfer: Syntax error")
                    return 

                for line in req:
                    if line.strip():
                        ses.write(line)
                ses.write(f'\nplaces:{places}\nstudents:\nwaitlist:{requestees}\n')
            self.delete(type="request")
            
            
    def SRChange(self,type:str,dataType:str,data:str):
        filedir = ""
        filelines = []
        if type == "session":
            filedir = f'sessions/{self.date}/{self.id}'
            dataTypes = ["time end","session type", "teacher Supervisor","equipment","places","students","waitlist"]
            if dataType not in dataTypes:
                print("Error in session change: 'dataType' Syntax error")
                return 
            
            if not self.filecheck():
                print("Error: file not found")
                return
        elif type == "request":
            filedir = f'sessionRequests/{self.date}{self.id}'
            dataTypes = ["requestees", "time end","session type", "teacher Supervisor","equipment"]
            if  dataType not in dataTypes:
                print("Error in request change: 'dataType' Syntax error")
                return 
            
            if not self.reqcheck():
                print("Error in request change: file not found")
                return
        else:
            print("Error in request change: syntax error")
            return
        
        with open(filedir, "r") as file:
            for line in file:
                if line.startswith(f"{dataType}:"):
                    line = f"{dataType}:{data}\n"
                filelines.append(line)

        with open(filedir, "w") as file:
            file.writelines(filelines)            
        

    def __str__(self):
        return f'date:{self.date}, time:{self.time}, id:{self.id}' 
      