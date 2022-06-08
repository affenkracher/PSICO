import math
from random import randint
import math
from modules.camera.camera import CameraLogger
from modules.micro.micro import MicroLogger
from modules.popup.popup import PopUp
from modules.music.music import MusicPlayer
from modules.task.task import Task


class SocialCreditController():
    def __init__(self, queryController) -> None:
        self.queryController = queryController
        self.socialCredit = queryController.getSCS()
        self.socialCreditScoreReference = queryController.getSCSReference()
        self.incriminitialReference = queryController.getIncriminitialReference()

    def main():
        pass

    def watch(self):
        self.socialCreditScoreReference.listen()

    def randomReaction(self):
        val = randint(0, 2)
        