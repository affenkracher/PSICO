from typing import List
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin.db import Reference
import os
import json
import base64

# https://firebase.google.com/docs/admin/setup#initialize-sdk
"""
Generate a unique connection to the firebase datastorage of PSICO, and return the reference
"""
def queryConnect():
    CWD = os.getcwd()
    CERTIFICATE_FILE_PATH = CWD + '\\PSICO-Buerger-Software\\res\\firebaseCertificate.json'
    CREDENTIALS = credentials.Certificate(CERTIFICATE_FILE_PATH)
    APP = firebase_admin.initialize_app(CREDENTIALS, options={
         'databaseURL': 'https://psico-software-default-rtdb.europe-west1.firebasedatabase.app/'
    })
    REF = db.reference("Citizen")
    return REF

"""
Central Data Handling class. Query, Update and Insert data.
"""
class QueryController():
    """
    Look for an existing entry id, if not create a new entry and save it inside the queryConfig.json inside the res folder
    """
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
        except:
            ID = self.insertQuery()
            dictionary = {
                "id": ID,
                "lastKeyLogId": 0
            }
            json_object = json.dumps(dictionary, indent=2)
            with open(f"{CWD}\\PSICO-Buerger-Software\\res\\queryConfig.json", "w") as configFile:
                configFile.write(json_object)
            self.queryId = ID
            self.lastKeyLogID = 0
            self.lastMouseLogID = 0

    """
    Safe the instance data of the query controller inside the queryConfig.json
    """
    def onClose(self):
        CWD = os.getcwd()
        try:
            with open(f"{CWD}\\PSICO-Buerger-Software\\res\\queryConfig.json", "w") as configFile:
                dictionary = {
                    "id": self.queryId,
                    "lastKeyLogId": self.lastKeyLogID,
                }
                json_object = json.dumps(dictionary, indent=2)
                configFile.write(json_object)
        except:
            print("Something went wrong")

    """
    Same as onClose, but only for specific key value pairs
    """
    def updateConfig(self, key, value):
        CWD = os.getcwd()
        try:
            json_object = None
            with open(f"{CWD}\\PSICO-Buerger-Software\\res\\queryConfig.json", "r") as configData:
                json_object = json.load(configData)
                configData.close()
            with open(f"{CWD}\\PSICO-Buerger-Software\\res\\queryConfig.json", "w") as configFile:
                json_object[key] = value
                json.dump(json_object, configFile, indent=2)
                configFile.close()
        except:
            print("Something went wrong")

    """
    On the query reference of Citizen create a new entry with these stats.
    The beginning social credit score is -100 cannot increase. The stored name is equal to the
    windows user name. Can be manually changed if so desired
    """
    def insertQuery(self):
        name = os.getlogin()
        CITIZEN_REF = self.connection.push({
            'Name': name,
            'SCS': -100,
            'Productivity': 0,
            'CPM': 0,
            'WPM': 0,
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
            'KeyEvaluation':
                {
                    '-1': 'Initial'
                }
        })
        return CITIZEN_REF.key

    """
    This method does not get used, its designed to be used inside the admin software
    """
    def selectQueryId(self, id):
        for DOC in self.connection.get():
            if DOC == id:
                CITIZEN_REF = self.connection.child(f'{DOC}')
                DATA_SET = CITIZEN_REF.get()
                if DATA_SET == None:
                    print("No Data Set found. Id is not known!")
                    return
                return DATA_SET

    """
    This method does not get used, its designed to be used inside the admin software
    """
    def selectQueryAll(self):
        query = []
        for DOC in self.connection.get():
            CITIZEN_REF = self.connection.child(f'{DOC}')
            DATA_SET = CITIZEN_REF.get()
            query.append(DATA_SET)
        return query

    """
    Add a list of strings to the KeyLogs field of the user. Assinges every entry an incrementing ID.
    """
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
    
    """
    Add the position and count of the users mouse to the MouseLogs field.
    If position is not known add new entry in field. If it is known, store old count
    and then add to it the new found count. Update the entry
    """
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
    
    """
    Add a base64 encoded string of a image to the CameraPictures field, can be decoded to
    view as png
    """
    def addToCameraLog(self, picture):
        CWD = os.getcwd()
        PICTURE_PATH = CWD + "\\PSICO-Buerger-Software\\modules\\camera\\storage\\test.png"
        CITIZEN_REF = self.connection.child(self.queryId)
        CAMERA_LOG_REF = CITIZEN_REF.child("CameraPictures")
        data = CAMERA_LOG_REF.get()
        dataLen = len(data)
        ID = dataLen % 5
        pictureToBase64 = base64.b64encode(picture).decode("ASCII")
        CAMERA_LOG_REF.update({
            ID: pictureToBase64
        })

    """
    Update the TaskLogs with the dictionary of (pid: taskName)
    """
    def addToTaskLog(self, log):
        CITIZEN_REF = self.connection.child(self.queryId)
        TASK_LOG_REF = CITIZEN_REF.child("TaskLogs")
        for data in log:
            id = data['pid']
            taskName = data['name']
            TASK_LOG_REF.update({
                id: taskName
            })

    def getSCS(self):
        CITIZEN_REF = self.connection.child(self.queryId)
        SCS = CITIZEN_REF.get()["SCS"]
        return SCS

    def updateSCS(self, value):
        CITIZEN_REF, SCS = self.getSCS()
        newSCS = SCS + value
        CITIZEN_REF.update({
            'SCS': newSCS
        })
        _, NEW_SCS = self.getSCS()
        print(NEW_SCS)

    def getSCSReference(self):
        CITIZEN_REF = self.connection.child(self.queryId)
        SCS_REF = CITIZEN_REF.child("SCS")
        return SCS_REF

    def getIncriminitialReference(self) -> Reference:
        CITIZEN_REF = self.connection.child(self.queryId)
        INCRIMINATING_REF = CITIZEN_REF.child("IncriminatingMaterial")
        return INCRIMINATING_REF