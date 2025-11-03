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
                raise SyntaxError("Error in function setId: Type syntax error.")
        else:
            raise Exception("ID already set")
            
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
                raise Exception(f'Error adding session: {e}')
            else:
                print(f"Session added succesfully with: {self.id}, time end:{timeEnd}\nsessions type:{self.type}\nteacher Supervisor:{teacher}\nequipment:{equipment}\nplaces:{places}\n")
        else:
            raise FileExistsError(f'Error session on {self.date}, of {self.type} at {self.time} already exists')
            

    def requestSession(self,user:str,timeEnd:str,teacherRequested:str,equipment=""):
        if  self.reqcheck():
            raise FileExistsError(f'Session request already made')
        elif self.filecheck():
            raise FileExistsError(f'Session file already exists')
        else:
            print("Creating request.")
            nl = "\n"
            try:
                with open(f'sessionRequests/{self.date}{self.id}','w') as f:
                    f.write(f'requestees:{user}\ntime end:{timeEnd}\nsession type:{self.type}\nteacher Supervisor:{teacherRequested}\nequipment:{equipment}')

            except Exception as e: 
                raise Exception(f"Error has occured in request session: \n{e}")
            else:
                print("Session request sucessfully made.")

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
                    raise FileNotFoundError(f"{sessionDirectory} Folder was not found")

                except Exception as e:
                    raise Exception(f'Error in delete function:\n {e} ')
            elif fileType == "file":
                try:
                    os.remove(f'{sessionDirectory}/{self.id}')
                except FileNotFoundError:
                    raise FileNotFoundError(f"Error: {sessionDirectory}/{self.id} doesnt exist.")
                except Exception as e:
                    raise Exception(f'Error in delete function:\n {e} ')
            else:
                raise Exception("ERROR in delete: fileType syntax error.")
        elif type == "request":
            try:
                os.remove(requestDirectory)
            except FileNotFoundError:
                raise FileNotFoundError(f"{requestDirectory} request not found.")
            except Exception as e:
                raise Exception(f'Error in delete function:\n {e} ')
            
    def requestTransfer(self,places=10,priorityPlaces=3):
        if self.filecheck():
            print("Session file already exists, removing request file.")
            self.delete(type="request")
        elif not self.reqcheck():
            raise FileNotFoundError("Request doesnt exist.")
        else:

            with open(f'sessionRequests/{self.date}{self.id}','r') as req, open(f'sessions/{self.date}/{self.id}', "w") as ses:
                # removes the unecesary requestees part and adds the requestees as people in the waitlist
                requestees = req.readline().strip()
                if requestees.startswith("requestees:"):
                    requestees = requestees.replace("requestees:", "", 1).strip()
                else:
                    raise SyntaxError("error in RequestTransfer: Syntax error")

                for line in req:
                    if line.strip():
                        ses.write(line)
                ses.write(f'\nplaces:{places}\nstudents:\nwaitlist:{requestees}\n')
            self.delete(type="request")
            
            
    def SRChange(self,type:str,dataType:str,data:str, add: bool = False):
        filedir = ""
        filelines = []
        changed = False

        if type == "session":
            filedir = f'sessions/{self.date}/{self.id}'
            dataTypes = ["time end","session type", "teacher Supervisor","equipment","places","students","waitlist"]
            if dataType not in dataTypes:
                raise SyntaxError("Error in session change: 'dataType' Syntax error")

            if not self.filecheck():
                raise FileNotFoundError("Error: file not found")

        elif type == "request":
            filedir = f'sessionRequests/{self.date}{self.id}'
            dataTypes = ["requestees", "time end","session type", "teacher Supervisor","equipment"]
            if dataType not in dataTypes:
                raise SyntaxError("Error in request change: 'dataType' Syntax error")

            if not self.reqcheck():
                raise FileNotFoundError("Error in request change: file not found")

        else:
            raise SyntaxError("Error in request change: syntax error")
        
        with open(filedir, "r") as file:
            for line in file:
                # split the first ':' to separate key and value
                if ':' in line:
                    key, rest = line.split(':', 1)
                    if key == dataType:
                        changed = True
                        current = rest.rstrip("\n")
                        if add:
                            # append with a comma if there is existing data
                            if current:
                                line = f"{dataType}:{current},{data}\n"
                            else:
                                line = f"{dataType}:{data}\n"
                        else:
                            line = f"{dataType}:{data}\n"
                filelines.append(line)

        if not changed:
            raise SyntaxError(f"No line found for dataType '{dataType}' in {filedir}")

        with open(filedir, "w") as file:
            file.writelines(filelines)            


    def __str__(self):
        return 