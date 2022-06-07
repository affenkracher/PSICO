import queryController

class Score():
    def __init__(self,  queryController):
        self.socialCreditScore = -100
        self.queryController = queryController
        
    def reduceScore(self, anzahl):
        self.socialCreditScore = self.socialCreditScore - anzahl

    def showScore(self):
        return self.socialCreditScore