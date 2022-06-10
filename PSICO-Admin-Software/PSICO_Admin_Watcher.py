import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import os

CWD = os.getcwd()

class AdminWatcher():

    def queryConnect(self):
        CERTIFICATE_FILE_PATH = CWD+'\\PSICO-Admin-Software\\res\\firebase-certificate.json'
        CRED = credentials.Certificate(CERTIFICATE_FILE_PATH)
        APP = firebase_admin.initialize_app(CRED, options = {'databaseURL':'https://psico-software-default-rtdb.europe-west1.firebasedatabase.app/'})
        ref = db.reference('Citizen')
        return ref

    def __init__(self) -> None:
        self.connection = self.queryConnect()
        self.allCitizenData = self.getAllCitizenInfo()

    def query(self):
        query = []
        for doc in self.connection.get():
            citizen_ref = self.connection.child(f'{doc}')
            data = citizen_ref.get()
            citizen_id = doc
            query.append((citizen_id, data))
        return query

    def getOneCitizen(self, id):
        for i, q in self.query(self):
            if(isinstance(q, dict)):
                if(i == id):
                    citizen = {'Name':q['Name'], 'SCS':q['SCS'], 'KPM':q['KPM'], 'CPM':q['CPM'], 'Failings':q['Failings']}
                    return citizen

    def getAllCitizenInfo(self):
        citizenList = []
        for i,q in self.query():
            if(isinstance(q, dict)):
                info = {'Name':q['Name'],'SCS':q['SCS'],'ID':i, 'KPM':q['KPM'], 'CPM':q['CPM'], 'Failings':q['Failings']}
                citizenList.append(info)
        return citizenList

    def updateCitizenData(self):
        while(self.operating == 1):
            time.sleep(30)
            self.allCitizenData = self.getAllCitizenInfo()

    def endUpdates(self):
        self.operating = 0


#    def calculateKeysPressed(Citizen):
#       parse keypresses
#       sort countings
#       return dictionary with keys times pressed

#   def calculateAllKeysPressed():
#       iterate calculateKeyPressed on all Citizen
#       return cumulated dictionary