import time
import random
from modules.camera.camera import CameraLogger
from modules.micro.micro import MicroLogger
from modules.popup.popup import PopUp
from modules.music.music import MusicPlayer
import keyboard

"""
AUTHOR: PHILIPP WENDEL
"""

RANDOM_STRINGS = ["Glorreiche Nation! ", "Super Kanzler! ", "Ich freue mich auf die nächste Indoktrination. ", "Heil meiner Nation. "]

"""
Controller Class to handle the behaviour of the indoctrination and punishment of citizens. Pulls the current social credit and evaluates the needed
steps to correct the documented behaviour.
"""

class SocialCreditController():
    def __init__(self, queryController, randStrings) -> None:
        self.queryController = queryController
        self.socialCredit = queryController.getSCS()
        self.oldSocialCredit = self.socialCredit
        self.socialCreditScoreReference = queryController.getSCSReference()
        self.randStrings = randStrings
        self.popup = PopUp()

    """
    Main method is an infinite loop pulling the SCS every minute, after that it starts some random action
    """

    def main(self):
        while 1:
            time.sleep(60)
            self.oldSocialCredit = self.socialCredit
            self.socialCredit = self.socialCreditScoreReference.get()
            diff = abs(self.socialCredit - self.oldSocialCredit)
            if diff != 0:
                self.popup.createPopUp("Social Credit Score Updated!", f'Dein neuer Social Credit Score ist {self.socialCredit}', 4)
            if diff % 10:
                self.randomReaction()
            if diff > 60:
                self.popup.createPopUp("HOER AUF", "WIR MERKEN UNS DEINE VERGEHEN. DU WIRST DAS TAGESLICHT NICHT MEHR SEHEN WERDEN", 60)
            q = abs(self.socialCredit // 4)
            if q > 1000:
                self.randomReaction()
            ran = random.randint(0, 1000)
            if ran < q:
                ranWord = random.choice(self.randStrings)
                keyboard.write(ranWord)

    """
    Helper method for main, start one of four possible actions
    """

    def randomReaction(self):
        r = random.randint(0,3)
        if r == 0:
            MP = MusicPlayer()
            MP.main()
        if r == 1:
            self.popup.main()
        if r == 2:
            CL = CameraLogger(self.queryController)
            CL.main()
        if r == 3:
            ML = MicroLogger(self.queryController)
            ML.main()
