import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# https://firebase.google.com/docs/admin/setup#initialize-sdk

cred = credentials.ApplicationDefault()
print(cred)
firebase_admin.initialize_app(cred, {
    'projectId': 'psico-software',
})

db = firestore.client()

USER_STORAGE_REF = db.collection(u'Citizen-Storage')
REF = USER_STORAGE_REF.stream()

for doc in REF:
    print(f'{doc.id} => {doc.to_dict()}')

class QueryController():
    def __init__(self) -> None:
        self.instance = 1

    def updateQuery(citizen):
        pass

    def insertQuery() -> int:
        pass

    def selectQuery(id):
        pass