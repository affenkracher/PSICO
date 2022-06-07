import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
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

#        self.citizen = hier alle Bürgerdaten holen
#        main()


    def getAllCitizen(self, ref):
        query = []
        for doc in ref.get():
            citizen_ref = ref.child(f'{doc}')
            data = citizen_ref.get()
            query.append(data)
        return query


#    getCitizen(id):
#       specitizen = self.citizen[id]
#       return specitizen

#    setSocialCredit(id, newSCP):
#       specitizen = getCitizen(id)
#       specitizen["scp"] = newSCP
#       in die Datenbank zurückschreiben
    
#    def buildHeatmap(coordinates):
#      calc coordinates together
#      build heatmap view
#      return heatmap

#    def calculateKeysPressed(Citizen):
#       parse keypresses
#       sort countings
#       return dictionary with keys times pressed

#   def calculateAllKeysPressed():
#       iterate calculateKeyPressed on all Citizen
#       return cumulated dictionary

#   def buildBigHeatmap():
#       iterate buildHeatmap on all Citizen
#       return cumulated heatmap

#   def main():
#       while(windowIsOpen):  