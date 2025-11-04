import os
import shutil
from filehandlers import getData, writeData, delete, createFile

class Session:
    def __init__(self, date:str, time:str, type:str):
        self.date = date #ddmmyy 
        self.time = time #hhmm
        self.type = type #physics, biology, chemistry
        self.id = None
        
        self.setId()
        os.makedirs("sessionRequests", exist_ok=True)
        os.makedirs("sessions",exist_ok=True)
        self.checkDateFile()
        
        self.reqdir = f'sessionRequests/{self.date}{self.id}'
        self.sesdir = f'sessions/{self.date}/{self.id}'

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
            
     
    def filecheck(self)-> bool:
        return os.path.exists(self.sesdir)
    def reqcheck(self) -> bool:
        return os.path.exists(self.reqdir)

    def checkDateFile(self):
        if not os.path.exists(f'sessions/{self.date}'):
            print(f"Added date folder for session of {self.date}")
            os.makedirs(f'sessions/{self.date}')

    def setSession(self, timeEnd:str, teacher:str,equipment:str, places=10, priorityPlaces=3):
        
        if not self.filecheck():
            try:    
                # with open(self.sesdir,'w') as f:
                #     f.write(f'time end:{timeEnd}\nsession type:{self.type}\nteacher Supervisor:{teacher}\nequipment:{equipment}\nplaces:{places}\nstudents:\nwaitlist:')
                params = {
                    "time end": timeEnd,
                    "session type": self.type,
                    "teacher Supervisor": teacher,
                    "equipment": equipment,
                    "places": str(places),
                    "students": "",
                    "waitlist": ""
                }
                createFile(self.sesdir, params)
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
                # with open(self.reqdir,'w') as f:
                #     f.write(f'requestees:{user}\ntime end:{timeEnd}\nsession type:{self.type}\nteacher Supervisor:{teacherRequested}\nequipment:{equipment}')
                params = {
                    "requestees": user,
                    "time end": timeEnd,
                    "session type": self.type,
                    "teacher Supervisor": teacherRequested,
                    "equipment": equipment
                }
                createFile(self.reqdir, params)
            except Exception as e: 
                raise Exception(f"Error has occured in request session: \n{e}")
            else:
                print("Session request sucessfully made.")

    def delete(self,fileType="file",type="session"):
        """
        Handles file and folder deletion\n
        params:\n
        fileType: ONLY for sessions, use either folder or file \n
        type: default = session, can change to request
        """
        directory = ''
        if type == "session":
            directory = f'sessions/{self.date}'
            if fileType == "folder":
                pass
            elif fileType == "file":
                directory = self.sesdir
            else:
                raise Exception("ERROR in delete: fileType syntax error.")
        elif type == "request":
            directory = self.reqdir
        else:
            raise Exception("ERROR in delete: type syntax error.")
        try:
            delete(directory,fileType)
        except FileNotFoundError:
            raise FileNotFoundError(f"{directory} not found.")
        except Exception as e:
            raise Exception(f'Error in delete function:\n {e} ')
        
    def requestTransfer(self,places=10,priorityPlaces=3):
        if self.filecheck():
            print("Session file already exists, removing request file.")
            self.delete(type="request")
        elif not self.reqcheck():
            raise FileNotFoundError("Request doesnt exist.")
        else:

            with open(self.reqdir,'r') as req, open(self.sesdir, "w") as ses:
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
            
            
    def SRChange(self,type:str,dataType:str,data:str, add: bool = False, remove:bool = False):
        # Determine file path and validate dataType
        if type == "session":
            filedir = self.sesdir
            dataTypes = ["time end","session type", "teacher Supervisor","equipment","places","students","waitlist"]
            if dataType not in dataTypes:
                raise SyntaxError("Error in session change: 'dataType' Syntax error")

            if not self.filecheck():
                raise FileNotFoundError("Error: file not found")

        elif type == "request":
            filedir = self.reqdir
            dataTypes = ["requestees", "time end","session type", "teacher Supervisor","equipment"]
            if dataType not in dataTypes:
                raise SyntaxError("Error in request change: 'dataType' Syntax error")

            if not self.reqcheck():
                raise FileNotFoundError("Error in request change: file not found")

        else:
            raise SyntaxError("Error in request change: syntax error")

        # Delegate actual update to writeData which reads/writes the file
        try:
            writeData(filedir, dataType, data, add=add, remove=remove)
        except KeyError:
            # map loader's KeyError to a more specific SyntaxError for callers
            raise SyntaxError(f"No line found for dataType '{dataType}' in {filedir}")
        except Exception as e:
            raise Exception(f"Error in SRChange:\n {e}")
    def SRGet(self, type:str, dataType:str)-> list:

        if type == "session":
            filedir = self.sesdir
            dataTypes = ["time end","session type", "teacher Supervisor","equipment","places","students","waitlist"]
            if dataType not in dataTypes:
                raise SyntaxError("Error in session get: 'dataType' Syntax error")
            if not self.filecheck():
                raise FileNotFoundError("Error: file not found")

        elif type == "request":
            filedir = self.reqdir
            dataTypes = ["requestees", "time end","session type", "teacher Supervisor","equipment"]
            if dataType not in dataTypes:
                raise SyntaxError("Error in request get: 'dataType' Syntax error")
            if not self.reqcheck():
                raise FileNotFoundError("Error in request get: file not found")
        else:
            raise SyntaxError("Error in SRGet: invalid type parameter")
        
        try:
            data = getData(filedir,dataType=dataType)
            print(data)
            return data
        except KeyError:
            raise SyntaxError(f"No line found for dataType '{dataType}' in {filedir}") #just in case
        except Exception as e:
            raise Exception(f"Error in SRGet:\n {e}")
        
    def cancelation(self,username:str, accountType:str):
        if accountType == "student":
            print("Initiating cancelation for student.")
            students = self.SRGet("session","students")
            waitlist = self.SRGet("session","waitlist")
            if username in students:
                students.remove(username)
                self.SRChange("session","students",",".join(students))
                print(f"{username} removed from session students.")

                if waitlist:
                    next_student = waitlist.pop(0)
                    self.SRChange("session","students",next_student,add=True)
                    self.SRChange("session","waitlist",",".join(waitlist))
                    print(f"{next_student} moved from waitlist to students.")
            elif username in waitlist:
                waitlist.remove(username)
                self.SRChange("session","waitlist",",".join(waitlist))
                print(f"{username} removed from waitlist.")
            else:
                print(f"{username} not found in students or waitlist.")
                raise Exception("error3")
            
        elif accountType == "teacher":
            print("Initiating cancelation for teacher supervisor.")
            current_teachers = self.SRGet("session","teacher Supervisor")
            if username in current_teachers:
                current_teachers.remove(username)
                self.SRChange("session","teacher Supervisor",",".join(current_teachers))
                print(f"{username} removed from teacher supervisors.")
            else:
                print(f"{username} not found in teacher supervisors.")
                raise Exception("error4")
            
            if current_teachers == []:
                print("No more teacher left in session, canceling session.")
                self.delete(fileType="file")

    def __str__(self):
        return 

