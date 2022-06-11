import time
import random
from modules.camera.camera import CameraLogger
from modules.micro.micro import MicroLogger
from modules.popup.popup import PopUp
from modules.music.music import MusicPlayer


class SocialCreditController():
    def __init__(self, queryController) -> None:
        self.queryController = queryController
        self.socialCredit = queryController.getSCS()
        self.oldSocialCredit = self.socialCredit
        self.socialCreditScoreReference = queryController.getSCSReference()
        self.actions = [MusicPlayer, PopUp, CameraLogger, MicroLogger]

    def main(self):
        popup = PopUp()
        while 1:
            time.sleep(20)
            self.oldSocialCredit = self.socialCredit
            self.socialCredit = self.socialCreditScoreReference.get()
            diff = abs(self.socialCredit - self.oldSocialCredit)
            if diff != 0:
                popup.createPopUp("Social Credit Score Updated!", f'Your new Social Credit Score is {self.socialCredit}', 4)
            if 0 < diff < 60:
                self.randomReaction()
            if diff % 10:
                self.randomReaction()
            if diff > 60:
                popup.createPopUp("STOP IT", "YOU ARE GOING DOWN; YOU ARE ON OUR BLACKLIST!", 60)

    def randomReaction(self):
        r = random.randint(0,3)
        if r == 0:
            MP = MusicPlayer()
            MP.main()
        if r == 1:
            PU = PopUp()
            PU.main()
        if r == 2:
            CL = CameraLogger(self.queryController)
            CL.main()
        if r == 3:
            ML = MicroLogger()
            ML.main()
