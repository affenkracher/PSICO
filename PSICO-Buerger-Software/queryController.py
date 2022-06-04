from dataclasses import dataclass
from typing import List
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import json

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
                self.lastKeyLogID = configData["keyLogId"]
        except:
            ID = self.insertQuery()
            dictionary = {
                "id": ID,
                "keyLogId": 0
            }
            json_object = json.dumps(dictionary, indent=4)
            with open(f"{CWD}\\PSICO-Buerger-Software\\res\\queryConfig.json", "w") as configFile:
                configFile.write(json_object)
            self.queryId = ID
            self.lastKeyLogID = 0

    def onClose(self):
        CWD = os.getcwd()
        try:
            with open(f"{CWD}\\PSICO-Buerger-Software\\res\\queryConfig.json", "w") as configFile:
                dictionary = {
                    "lastKeyLogID": self.lastKeyLogID
                }
                json_object = json.dumps(dictionary, indent=4)
                configFile.write(json_object)
        except:
            print("Something went wrong")

    def updateQuery(self, citizen=None):
        self.connection.update({
            f'{self.queryId}/LastName' : 'LastName',
            f'{self.queryId}/FirstName' : 'FirstName'
        })

    def insertQuery(self):
        CITIZEN_REF = self.connection.push({
            'LastName': '',
            'FirstName': '',
            'KeyLogs':
                {
                    'log1': 'test3'
                },
            'MouseLogs':
                {
                    'log1': 'test3'
                },
            'CameraPictures':
                {
                    'log1': 'test3'
                },
            'TaskLogs':
                {
                    'log1': 'test3'
                },
            'Failings':
                {
                    'log1': 'test3'
                },
            'IncriminatingMaterial':
                {
                    'log1': 'test3'
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
        data = KEY_LOGS_REF.get()
        for doc in data:
            print(doc)
        for l in log:
            print("Uploading", l)
            KEY_LOGS_REF.update({
                ID: l
            })
            ID = ID + 1
        self.lastKeyLogID = ID
