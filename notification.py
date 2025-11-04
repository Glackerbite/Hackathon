import os 

class Notifications:
    def __init__(self):

        os.makedirs(f"notifications", exist_ok=True)
        os.makedirs(f"notifications/alerts", exist_ok=True)
        os.makedirs(f"notifications/requests", exist_ok=True)
    
    def checkDateFile(self, date, location:str):
        if not os.path.exists(f'notidfcations/{location}{date}'):
            print(f"Added date folder for session of {self.date}")
            os.makedirs(f'noti/{self.date}')
