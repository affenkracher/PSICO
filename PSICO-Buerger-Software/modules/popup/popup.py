from win10toast import ToastNotifier
import random
import time

"""
Creating a new windows 10 popup with a message, title and duration. Automatically
disappears after the duration has run out
"""
class PopUp():
    def __init__(self):
        self.alive = 1
        self.messages = ["Work harder!", "Work better!", "Work stronger!", "Stay focused!", "Stay awake!"]
        self.titles = ["Big Brother is Watching", "We what you did"]

    def createPopUp(self, title, msg, duration,):
        toaster = ToastNotifier()
        """
        By active Focus Assistent "Priority Only" PopUps wont appear
        """
        toaster.show_toast(title, msg, duration=duration)

    def main(self):
        title = random.choice(self.titles)
        message = random.choice(self.messages)
        duration = random.randint(4, 10)
        self.createPopUp(title, message, duration)

    def productivityEnhancement(self):
        motivationalTexts = ["KEEP YOUR SPIRIT AND WORK HARD", "WE NEED YOU TO WORK: DO YOUR BEST", "Success is not final; failure is not fatal: It is the courage to (**INSERT COMPLIANT TEXT HERE**) that counts.", "It is better to fail in originality than to succeed in imitation.", "Success usually comes to those who are too busy looking for it.", "Develop success from failures. Discouragement and failure are two of the surest stepping stones to success."]
        while 1:
            time.sleep(5 * 60)
            txt = random.choice(motivationalTexts)
            self.createPopUp("Do Your Best for our Grand Nation!", txt, 7)