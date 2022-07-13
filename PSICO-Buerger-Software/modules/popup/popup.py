from win10toast import ToastNotifier
import random
import time

"""
AUTHOR: MAHMOUD ALMASRI, PHILIPP WENDEL
"""

"""
Creating a new windows 10 popup with a message, title and duration. Automatically
disappears after the duration has run out
"""
class PopUp():
    def __init__(self):
        self.alive = 1
        self.messages = ["Sei schneller!", "Arbeite genauer!", "Work stronger!", "Bleib Fokussiert!", "Schlaf ist überbewertet!"]
        self.titles = ["Big Brother sieht dein Handeln!", "Wir wissen was du tust!", "Versuche erst garnicht uns zu hintergehen!"]
        self.toaster = ToastNotifier()

    def createPopUp(self, title, msg, duration,):
        """
        By active Focus Assistent "Priority Only" PopUps wont appear
        """
        try:
            self.toaster.show_toast(title, msg, duration=duration)
        except:
            pass

    def main(self):
        title = random.choice(self.titles)
        message = random.choice(self.messages)
        duration = random.randint(4, 10)
        self.createPopUp(title, message, duration)

    def productivityEnhancement(self):
        motivationalTexts = ["BEWAHREN SIE IHREN GEIST UND ARBEITEN SIE HART", "WIR BRAUCHEN SIE ZUM ARBEITEN: TUN SIE IHR BESTES", "Erfolg ist nicht endgültig; Misserfolg ist nicht tödlich: Es ist der Mut zu (**HIER KOMPLIZITEN TEXT EINFÜGEN**), der zählt.", "Es ist besser, in der Originalität zu scheitern, als in der Nachahmung erfolgreich zu sein.", "Erfolg kommt meist zu denen, die zu sehr damit beschäftigt sind, ihn zu suchen.", "Entwickeln Sie Erfolg aus Misserfolgen. Entmutigung und Misserfolg sind zwei der sichersten Trittsteine zum Erfolg."]
        while 1:
            time.sleep(5 * 60)
            txt = random.choice(motivationalTexts)
            self.createPopUp("Tue dein Bestes für unsere glorreiche Nation!", txt, 7)