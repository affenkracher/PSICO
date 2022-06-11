import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
        self.countCitizen = 0
        self.koa = 0
        self.coa = 0
        self.kavg = 0
        self.cavg = 0
        self.scsall = 0
        self.scsavg = 0
        self.failings = 0
        self.failingsavg = 0
        self.connection = self.queryConnect()
        self.allCitizenData = []
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
                if(i != 'Citizen1'):
                    info = {'Name':q['Name'],'SCS':q['SCS'],'ID':i, 'KPM':q['KPM'], 'CPM':q['CPM'], 'Failings':q['Failings']}
                    citizenList.append(info)
                    self.countCitizen += 1
                    self.koa += q['KOA']
                    self.coa += q['COA']
                    self.scsall += q['SCS']
                    self.failings += len(q['Failings'])
                
        self.kavg = self.koa / self.countCitizen
        self.cavg = self.coa / self.countCitizen
        self.failingsavg = self.failings / self.countCitizen
        self.scsavg = self.scsall / self.countCitizen

        return citizenList

    def updateCitizenData(self):
        while(self.operating == 1):
            time.sleep(30)
            self.allCitizenData = self.getAllCitizenInfo()

    def endUpdates(self):
        self.operating = 0
        
    def generateHeatmap(self, dictionary):
        ser = pd.Series(list(dictionary.values()), index=pd.MultiIndex.from_tuples(dictionary.keys()))
        dataframe = ser.unstack().fillna(0)
        sns.set(rc = {'figure.figsize':(12.8,7.2)})
        sns.heatmap(dataframe, xticklabels=False, yticklabels=False, cbar=False, vmin=0, vmax=200, cmap="rocket")
        # plt.savefig('output.png')
        plt.show()
    
    def getComulatedMouseData(self):
        keys = [*self.connection.get()][:-1]
        mouseData = {}
        for key in keys:
            CITIZEN_REF = self.connection.child(key)
            MOUSE_LOGS_REF = CITIZEN_REF.child("MouseLogs")
            mousePositions = [*MOUSE_LOGS_REF.get()]
            data = MOUSE_LOGS_REF.get()
            for pos in mousePositions: 
                if pos == '-1':
                    continue
                freq = data[pos]
                temp1 = pos[1:-1].split(',')
                x = int(temp1[0])
                y = int(temp1[1])
                if (x,y) in mouseData:
                    mouseData[(x,y)] = mouseData[(x,y)] + freq
                else:
                    mouseData[(x,y)] = freq
        return mouseData
    
    def getCitizenMouseData(self, citizenId):
        print(citizenId)
        mouseData = {}
        CITIZEN_REF = self.connection.child(citizenId)
        MOUSE_LOGS_REF = CITIZEN_REF.child("MouseLogs")
        mousePositions = [*MOUSE_LOGS_REF.get()]
        data = MOUSE_LOGS_REF.get()
        for pos in mousePositions: 
            if pos == '-1':
                continue
            freq = data[pos]
            temp1 = pos[1:-1].split(',')
            x = int(temp1[0])
            y = int(temp1[1])
            if (x,y) in mouseData:
                mouseData[(x,y)] = mouseData[(x,y)] + freq
            else:
                mouseData[(x,y)] = freq
        return mouseData


#    def calculateKeysPressed(Citizen):
#       parse keypresses
#       sort countings
#       return dictionary with keys times pressed

#   def calculateAllKeysPressed():
#       iterate calculateKeyPressed on all Citizen
#       return cumulated dictionary