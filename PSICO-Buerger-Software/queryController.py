from typing import List
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, storage
from firebase_admin.db import Reference
import os
import json

def getCWD():
    CWD = os.getcwd()
    if CWD.find("\\PSICO-Buerger-Software") >= 0:
        cut = len("\\PSICO-Buerger-Software")
        CWD = CWD[0:-cut]
    return CWD

# https://firebase.google.com/docs/admin/setup#initialize-sdk
"""
Generate a unique connection to the firebase datastorage of PSICO, and return the reference
"""
def queryConnect():
    CWD = getCWD()
    CERTIFICATE_FILE_PATH = CWD + '\\PSICO-Buerger-Software\\res\\firebaseCertificate.json'
    CREDENTIALS = credentials.Certificate(CERTIFICATE_FILE_PATH)
    APP = firebase_admin.initialize_app(CREDENTIALS, options={
         'databaseURL': 'https://psico-software-default-rtdb.europe-west1.firebasedatabase.app/'
    })
    REF = db.reference("Citizen")
    return REF

def storageConnect():
    CWD = getCWD()
    CERTIFICATE_FILE_PATH = CWD + '\\PSICO-Buerger-Software\\res\\firebaseCertificate.json'
    CREDENTIALS = credentials.Certificate(CERTIFICATE_FILE_PATH)
    OTHER_APP = firebase_admin.initialize_app(CREDENTIALS, options={
        'projectId': 'psico-software',
        'storageBucket': 'psico-software.appspot.com'
    }, name="app2")
    BUCKET = storage.bucket(app=OTHER_APP)
    return BUCKET

"""
Central Data Handling class. Query, Update and Insert data.
"""
class QueryController():
    """
    Look for an existing entry id, if not create a new entry and save it inside the queryConfig.json inside the res folder
    """
    def __init__(self) -> None:
        self.alive = True
        self.storage = storageConnect()
        self.connection = queryConnect()
        CWD = getCWD()
        try:
            with open(f"{CWD}\\PSICO-Buerger-Software\\res\\queryConfig.json", "r") as configFile:
                configData = json.load(configFile)
                self.queryId = configData["id"]
                print(self.queryId)
                self.lastKeyLogID = configData["lastKeyLogId"]
                self.lastImgID = configData["lastImgId"]
                self.lastAudioID = configData["lastAudioId"]
        except:
            ID = self.insertQuery()
            dictionary = {
                "id": ID,
                "lastKeyLogId": 0,
                "lastImgId": 0,
                "lastAudioId": 0,
            }
            json_object = json.dumps(dictionary, indent=2)
            with open(f"{CWD}\\PSICO-Buerger-Software\\res\\queryConfig.json", "w") as configFile:
                configFile.write(json_object)
            self.queryId = ID
            self.lastKeyLogID = 0
            self.lastImgID = 0
            self.lastAudioID = 0
        self.CITIZEN_REF = self.connection.child(self.queryId)

    """
    Safe the instance data of the query controller inside the queryConfig.json
    """
    def onClose(self):
        CWD = getCWD()
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
        CWD = getCWD()
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
            'SCS': -10,
            'Productivity': 0,
            'CPM': 0,
            'WPM': 0,
            'KPM': 0,
            'KeyLogs':
                {
                    '-1': 'Initial'
                },
            'MouseLogs':
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
                },
            'AudioLogs': 
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
        KEY_LOGS_REF = self.CITIZEN_REF.child("KeyLogs")
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
        MOUSE_LOGS_REF = self.CITIZEN_REF.child("MouseLogs")
        for k1 in log:
            dbVal = MOUSE_LOGS_REF.child(k1).get()
            if dbVal is None:
                print("First", log[k1])
                MOUSE_LOGS_REF.update({
                    k1: log[k1]
                })
            else:
                newVal = int(log[k1]) + int(dbVal)
                print("Update", log[k1])
                MOUSE_LOGS_REF.update({
                    k1: newVal
                })
    
    """
    Add a base64 encoded string of a image to the CameraPictures field, can be decoded to
    view as png
    """
    def addToCameraLog(self, picture):
        blob = self.storage.blob(picture)
        blob.upload_from_filename(filename=picture, content_type="image/png")

    """
    Update the TaskLogs with the dictionary of (pid: taskName)
    """
    def addToTaskLog(self, log):
        TASK_LOG_REF = self.CITIZEN_REF.child("TaskLogs")
        for data in log:
            id = data['pid']
            taskName = data['name']
            TASK_LOG_REF.update({
                id: taskName
            })

    def getSCS(self):
        SCS = self.CITIZEN_REF.get()["SCS"]
        return SCS

    def updateSCS(self, value):
        SCS = self.getSCS()
        newSCS = SCS + value
        self.CITIZEN_REF.update({
            'SCS': newSCS
        })
        NEW_SCS = self.getSCS()
        print(NEW_SCS)

    def getSCSReference(self):
        SCS_REF = self.CITIZEN_REF.child("SCS")
        return SCS_REF

    def getIncriminitialReference(self) -> Reference:
        INCRIMINATING_REF = self.CITIZEN_REF.child("Failings")
        return INCRIMINATING_REF

    def saveBadHabits(self, badHabit):
        REF = self.getIncriminitialReference()
        key = len([*REF.get()])
        REF.update({
            key: badHabit
        })

    def updateKeyEvaluation(self, keyEvaluation):
        KEYEVALUATION_REF = self.CITIZEN_REF.child("KeyEvaluation")
        for k1 in keyEvaluation:
            dbVal = KEYEVALUATION_REF.child(k1).get()
            if dbVal is None:
                KEYEVALUATION_REF.update({
                    k1: keyEvaluation[k1]
                })
            else:
                newVal = int(dbVal) + int(keyEvaluation[k1])
                KEYEVALUATION_REF.update({
                    k1: newVal
                })

    def updateCurrentWPM(self, wpm):
        self.CITIZEN_REF.update({
            "WPM": wpm
        })

    def updateKPM(self, kpm): 
        self.CITIZEN_REF.update({
            "KPM": kpm
        })

    def updateCPM(self, cpm): 
        self.CITIZEN_REF.update({
            "CPM": cpm
        })

    def uploadAudio(self, audio): 
        blob = self.storage.blob(audio)
        blob.upload_from_filename(filename=audio, content_type="audio/wav")