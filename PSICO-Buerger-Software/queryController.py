import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import db
import os

# https://firebase.google.com/docs/admin/setup#initialize-sdk

cwd = os.getcwd()

certificateFilePath = cwd + '\\PSICO-Buerger-Software\\res\\firestoreCertificate.json'

cred = credentials.Certificate(certificateFilePath)

psico_app = firebase_admin.initialize_app(cred, options={
    'projectId': 'psico-software'
})

database = firestore.client(psico_app)

USER_STORAGE_REF = database.collection(u'Citizen-Storage')
REF = USER_STORAGE_REF.get()

for doc in REF:
    print(f'{doc.id} => {doc.to_dict()}')
    

class QueryController():
    def __init__(self) -> None:
        self.alive = True

    def updateQuery(citizen):
        pass

    def insertQuery():
        pass

    def selectQuery(id):
        pass