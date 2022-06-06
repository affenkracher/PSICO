from typing import List
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import json
import base64

# https://firebase.google.com/docs/admin/setup#initialize-sdk

def queryConnect():
    CWD = os.getcwd()
    CERTIFICATE_FILE_PATH = CWD + '\\PSICO-Buerger-Software\\res\\firebaseCertificate.json'
    CREDENTIALS = credentials.Certificate(CERTIFICATE_FILE_PATH)
    APP = firebase_admin.initialize_app(CREDENTIALS, options={
         'databaseURL': 'https://psico-software-default-rtdb.europe-west1.firebasedatabase.app/'
    })
    REF = db.reference("Citizen")
    return REF

class QueryController():
    def __init__(self) -> None:
        self.alive = True
        self.connection = queryConnect()
        CWD = os.getcwd()
        try:
            with open(f"{CWD}\\PSICO-Buerger-Software\\res\\queryConfig.json", "r") as configFile:
                configData = json.load(configFile)
                self.queryId = configData["id"]
                print(self.queryId)
                self.lastKeyLogID = configData["lastKeyLogId"]
                self.lastMouseLogID = configData["lastMouseLogId"]
        except:
            ID = self.insertQuery()
            dictionary = {
                "id": ID,
                "lastKeyLogId": 0,
                "lastMouseLogId": 0
            }
            json_object = json.dumps(dictionary, indent=2)
            with open(f"{CWD}\\PSICO-Buerger-Software\\res\\queryConfig.json", "w") as configFile:
                configFile.write(json_object)
            self.queryId = ID
            self.lastKeyLogID = 0
            self.lastMouseLogID = 0

    def onClose(self):
        CWD = os.getcwd()
        try:
            with open(f"{CWD}\\PSICO-Buerger-Software\\res\\queryConfig.json", "w") as configFile:
                dictionary = {
                    "lastKeyLogId": self.lastKeyLogID,
                    "lastMouseLogId": self.lastMouseLogID
                }
                json_object = json.dumps(dictionary, indent=2)
                configFile.write(json_object)
        except:
            print("Something went wrong")

    def updateConfig(self, key, value):
        CWD = os.getcwd()
        try:
            json_object = None
            with open(f"{CWD}\\PSICO-Buerger-Software\\res\\queryConfig.json", "r") as configData:
                json_object = json.load(configData)
                configData.close()
            with open(f"{CWD}\\PSICO-Buerger-Software\\res\\queryConfig.json", "w") as configFile:
                json_object[key] = value
                json.dump(json_object, configFile)
                configFile.close()
        except:
            print("Something went wrong")

    def updateQuery(self, citizen=None):
        self.connection.update({
            f'{self.queryId}/LastName' : 'LastName',
            f'{self.queryId}/FirstName' : 'FirstName'
        })

    def insertQuery(self):
        name = os.getlogin()
        CITIZEN_REF = self.connection.push({
            'Name': name,
            'SCS': -100,
            'Productivity': 0,
            'KeyLogs':
                {
                    '-1': 'Initial'
                },
            'MouseLogs':
                {
                    '-1': 'Initial'
                },
            'CameraPictures':
                {
                    '-1': 'Initial'
                },
            'TaskLogs':
                {
                    '-1': 'Initial'
                },
            'Failings':
                {
                    '-1': 'Initial'
                },
            'IncriminatingMaterial':
                {
                    '-1': 'Initial'
                },
        })
        return CITIZEN_REF.key

    def selectQueryId(self, id):
        for DOC in self.connection.get():
            if DOC == id:
                CITIZEN_REF = self.connection.child(f'{DOC}')
                DATA_SET = CITIZEN_REF.get()
                if DATA_SET == None:
                    print("No Data Set found. Id is not known!")
                    return
                return DATA_SET

    def selectQueryAll(self):
        query = []
        for DOC in self.connection.get():
            CITIZEN_REF = self.connection.child(f'{DOC}')
            DATA_SET = CITIZEN_REF.get()
            query.append(DATA_SET)
        return query

    def addToKeyLogs(self, log: List[str]):
        CITIZEN_REF = self.connection.child(self.queryId)
        KEY_LOGS_REF = CITIZEN_REF.child("KeyLogs")
        ID = self.lastKeyLogID
        for l in log:
            print("Uploading", l)
            KEY_LOGS_REF.update({
                ID: l
            })
            ID = ID + 1
        self.lastKeyLogID = ID
        self.updateConfig("lastKeyLogId", ID)
    
    def addToMouseLogs(self, log):
        CITIZEN_REF = self.connection.child(self.queryId)
        MOUSE_LOGS_REF = CITIZEN_REF.child("MouseLogs")
        for k1 in log:
            dbVal = MOUSE_LOGS_REF.child(k1).get()
            if dbVal is None:
                print("initial upload", k1)
                MOUSE_LOGS_REF.update({
                    k1: log[k1]
                })
            else:
                print("erhöhe counter ")
                newVal = int(log[k1]) + int(dbVal)
                MOUSE_LOGS_REF.update({
                    k1: newVal
                })
    
    def addToCameraLog(self, picture):
        CITIZEN_REF = self.connection.child(self.queryId)
        CAMERA_LOG_REF = CITIZEN_REF.child("CameraPictures")
        data = CAMERA_LOG_REF.get()
        dataLen = len(data)
        ID = dataLen
        if dataLen % 5 == 0:
            ID = 0
        pictureToBase64 = base64.b64encode(picture)
        CAMERA_LOG_REF.update({
            ID: pictureToBase64
        })
