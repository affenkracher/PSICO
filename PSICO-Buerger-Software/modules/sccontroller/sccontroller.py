import time
import random
from modules.camera.camera import CameraLogger
from modules.micro.micro import MicroLogger
from modules.popup.popup import PopUp
from modules.music.music import MusicPlayer
import keyboard

RANDOM_STRINGS = ["Glorreiche Nation! ", "Super Kanzler! ", "Ich freue mich auf die nächste Indoktrination. ", "Heil meiner Nation. "]

class SocialCreditController():
    def __init__(self, queryController, randStrings) -> None:
        self.queryController = queryController
        self.socialCredit = queryController.getSCS()
        self.oldSocialCredit = self.socialCredit
        self.socialCreditScoreReference = queryController.getSCSReference()
        self.randStrings = randStrings
        self.popup = PopUp()

    def main(self):
        while 1:
            time.sleep(60)
            self.oldSocialCredit = self.socialCredit
            self.socialCredit = self.socialCreditScoreReference.get()
            print(self.socialCredit)
            diff = abs(self.socialCredit - self.oldSocialCredit)
            if diff != 0:
                self.popup.createPopUp("Social Credit Score Updated!", f'Your new Social Credit Score is {self.socialCredit}', 4)
            if diff % 10:
                self.randomReaction()
            if diff > 60:
                self.popup.createPopUp("STOP IT", "YOU ARE GOING DOWN. YOU ARE ON OUR BLACKLIST!", 60)
            q = abs(self.socialCredit // 4)
            if q > 1000:
                self.randomReaction()
            ran = random.randint(0, 1000)
            if ran < q:
                ranWord = random.choice(self.randStrings)
                keyboard.write(ranWord)

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
